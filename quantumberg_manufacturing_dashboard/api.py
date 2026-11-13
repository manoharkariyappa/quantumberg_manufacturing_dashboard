import frappe
from frappe.utils import add_days, flt, getdate, nowdate


def _date_range(period="Last 30 Days"):
    """Return the start and end dates for a dashboard period."""
    end_date = getdate(nowdate())

    days = {
        "Last 7 Days": 7,
        "Last 30 Days": 30,
        "Last 90 Days": 90,
        "Last Year": 365,
    }.get(period, 30)

    return add_days(end_date, -(days - 1)), end_date


def _resolve_dates(from_date=None, to_date=None, period="Last 30 Days"):
    if from_date and to_date:
        return getdate(from_date), getdate(to_date)

    return _date_range(period)


def _has_doctype(doctype):
    return bool(frappe.db.exists("DocType", doctype))


def _has_field(doctype, fieldname):
    if not _has_doctype(doctype):
        return False

    return fieldname in frappe.get_meta(doctype).get_valid_columns()


def _count(doctype, filters=None):
    if not _has_doctype(doctype):
        return 0

    return frappe.db.count(doctype, filters=filters or {})


def _success(data):
    return {"success": True, "data": data}


def _date_filters(
    doctype,
    field,
    start_date,
    end_date,
    company=None,
    datetime_field=False,
):
    if datetime_field:
        value = [f"{start_date} 00:00:00", f"{end_date} 23:59:59"]
    else:
        value = [str(start_date), str(end_date)]

    filters = {field: ["between", value]}

    if company and _has_field(doctype, "company"):
        filters["company"] = company

    return filters


def _sql_conditions(doctype, date_field, start_date, end_date, company=None):
    conditions = [f"DATE(`{date_field}`) BETWEEN %(start_date)s AND %(end_date)s"]
    params = {"start_date": start_date, "end_date": end_date}

    if company and _has_field(doctype, "company"):
        conditions.append("company = %(company)s")
        params["company"] = company

    return " AND ".join(conditions), params


@frappe.whitelist()
def get_dashboard_summary(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    start_date, end_date = _resolve_dates(from_date, to_date, period)

    empty = {
        "open_work_orders": 0,
        "wip_work_orders": 0,
        "manufactured_items_value": 0,
        "items_in_production": 0,
    }

    if not _has_doctype("Work Order"):
        return _success(empty)

    filters = _date_filters(
        "Work Order",
        "creation",
        start_date,
        end_date,
        company,
        datetime_field=True,
    )
    filters["docstatus"] = 1

    open_count = _count(
        "Work Order",
        {
            **filters,
            "status": [
                "in",
                [
                    "Not Started",
                    "Open",
                    "In Process",
                    "Stock Reserved",
                    "Stock Partially Reserved",
                ],
            ],
        },
    )

    wip_count = _count("Work Order", {**filters, "status": "In Process"})

    active_orders = frappe.get_all(
        "Work Order",
        filters={
            **filters,
            "status": ["in", ["Not Started", "Open", "In Process", "Stock Reserved", "Stock Partially Reserved"]],
        },
        fields=["production_item"],
        limit_page_length=0,
    )

    items_in_production = len(
        {row.production_item for row in active_orders if row.production_item}
    )

    value_orders = frappe.get_all(
        "Work Order",
        filters=filters,
        fields=["production_item", "produced_qty"],
        limit_page_length=0,
    )

    item_codes = {
        row.production_item for row in value_orders if row.production_item
    }
    valuation = {}

    if item_codes:
        for item in frappe.get_all(
            "Item",
            filters={"name": ["in", list(item_codes)]},
            fields=["name", "valuation_rate"],
            limit_page_length=0,
        ):
            valuation[item.name] = flt(item.valuation_rate)

    manufactured_value = sum(
        flt(row.produced_qty) * valuation.get(row.production_item, 0)
        for row in value_orders
    )

    return _success({
        "open_work_orders": open_count,
        "wip_work_orders": wip_count,
        "manufactured_items_value": manufactured_value,
        "items_in_production": items_in_production,
    })


@frappe.whitelist()
def get_work_order_analysis(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    if not _has_doctype("Work Order"):
        return _success({"labels": [], "values": []})

    start_date, end_date = _resolve_dates(from_date, to_date, period)
    where, params = _sql_conditions(
        "Work Order", "creation", start_date, end_date, company
    )

    rows = frappe.db.sql(f"""
        SELECT status, COUNT(*) AS total
        FROM `tabWork Order`
        WHERE {where} AND docstatus = 1
        GROUP BY status
        ORDER BY total DESC
    """, params, as_dict=True)

    return _success({
        "labels": [row.status or "Unknown" for row in rows],
        "values": [row.total for row in rows],
    })


@frappe.whitelist()
def get_job_card_analysis(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    if not _has_doctype("Job Card"):
        return _success({"categories": [], "series": []})

    start_date, end_date = _resolve_dates(from_date, to_date, period)
    where, params = _sql_conditions(
        "Job Card", "posting_date", start_date, end_date, company
    )

    rows = frappe.db.sql(f"""
        SELECT
            DATE_FORMAT(posting_date, '%%Y-%%m') AS month,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
            SUM(
                CASE
                    WHEN status IN ('Open', 'Work In Progress', 'Pending')
                    THEN 1 ELSE 0
                END
            ) AS pending
        FROM `tabJob Card`
        WHERE {where} AND docstatus < 2
        GROUP BY month
        ORDER BY month
    """, params, as_dict=True)

    return _success({
        "categories": [row.month for row in rows],
        "series": [
            {
                "name": "Completed",
                "data": [int(row.completed) for row in rows],
            },
            {
                "name": "Pending",
                "data": [int(row.pending) for row in rows],
            },
        ],
    })


@frappe.whitelist()
def get_produced_quantity(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    if not _has_doctype("Work Order"):
        return _success({"labels": [], "planned": [], "produced": []})

    start_date, end_date = _resolve_dates(from_date, to_date, period)
    where, params = _sql_conditions(
        "Work Order", "creation", start_date, end_date, company
    )

    rows = frappe.db.sql(f"""
        SELECT
            DATE(creation) AS production_date,
            SUM(COALESCE(qty, 0)) AS planned,
            SUM(COALESCE(produced_qty, 0)) AS produced
        FROM `tabWork Order`
        WHERE {where} AND docstatus = 1
        GROUP BY DATE(creation)
        ORDER BY production_date
    """, params, as_dict=True)

    return _success({
        "labels": [str(row.production_date) for row in rows],
        "planned": [flt(row.planned) for row in rows],
        "produced": [flt(row.produced) for row in rows],
    })


@frappe.whitelist()
def get_completed_operations(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    if not _has_doctype("Job Card"):
        return _success({"labels": ["Completed", "Pending"], "values": [0, 0]})

    start_date, end_date = _resolve_dates(from_date, to_date, period)
    filters = _date_filters(
        "Job Card", "posting_date", start_date, end_date, company
    )
    filters["docstatus"] = ["<", 2]

    completed = _count("Job Card", {**filters, "status": "Completed"})
    pending = _count(
        "Job Card",
        {
            **filters,
            "status": ["in", ["Open", "Work In Progress", "Pending"]],
        },
    )

    return _success({
        "labels": ["Completed", "Pending"],
        "values": [completed, pending],
    })


@frappe.whitelist()
def get_work_order_quantity(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    if not _has_doctype("Work Order"):
        return _success({"labels": [], "planned": [], "produced": []})

    start_date, end_date = _resolve_dates(from_date, to_date, period)
    filters = _date_filters(
        "Work Order",
        "creation",
        start_date,
        end_date,
        company,
        datetime_field=True,
    )
    filters["docstatus"] = 1

    rows = frappe.get_all(
        "Work Order",
        filters=filters,
        fields=["name", "production_item", "qty", "produced_qty"],
        order_by="creation desc",
        limit_page_length=10,
    )

    return _success({
        "labels": [
            f"{row.production_item or row.name}" for row in rows
        ],
        "planned": [flt(row.qty) for row in rows],
        "produced": [flt(row.produced_qty) for row in rows],
    })


@frappe.whitelist()
def get_pending_work_orders(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    if not _has_doctype("Work Order"):
        return _success({"labels": [], "values": []})

    start_date, end_date = _resolve_dates(from_date, to_date, period)
    filters = _date_filters(
        "Work Order",
        "creation",
        start_date,
        end_date,
        company,
        datetime_field=True,
    )
    filters["docstatus"] = 1
    filters["status"] = [
        "in",
        [
            "Not Started",
            "Open",
            "In Process",
            "Stock Reserved",
            "Stock Partially Reserved",
        ],
    ]

    rows = frappe.get_all(
        "Work Order",
        filters=filters,
        fields=["name", "production_item", "qty", "produced_qty"],
        order_by="creation desc",
        limit_page_length=10,
    )

    return _success({
        "labels": [row.production_item or row.name for row in rows],
        "values": [
            max(flt(row.qty) - flt(row.produced_qty), 0)
            for row in rows
        ],
    })


@frappe.whitelist()
def get_quality_inspection_analysis(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    if not _has_doctype("Quality Inspection"):
        return _success({"labels": [], "values": []})

    start_date, end_date = _resolve_dates(from_date, to_date, period)
    where, params = _sql_conditions(
        "Quality Inspection", "creation", start_date, end_date, company
    )

    rows = frappe.db.sql(f"""
        SELECT status, COUNT(*) AS total
        FROM `tabQuality Inspection`
        WHERE {where} AND docstatus < 2
        GROUP BY status
        ORDER BY total DESC
    """, params, as_dict=True)

    return _success({
        "labels": [row.status or "Unknown" for row in rows],
        "values": [row.total for row in rows],
    })


@frappe.whitelist()
def get_downtime_analysis(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    # ERPNext does not have a universal downtime DocType across installations.
    # Return an empty chart until a configured downtime source is identified.
    return _success({
        "labels": [],
        "values": [],
        "message": "Configure a machine downtime source to display this chart.",
    })


@frappe.whitelist()
def get_manufacturing_reports(
    from_date=None,
    to_date=None,
    company=None,
    period="Last 30 Days",
):
    if not _has_doctype("Work Order"):
        return _success([])

    start_date, end_date = _resolve_dates(from_date, to_date, period)
    filters = _date_filters(
        "Work Order",
        "creation",
        start_date,
        end_date,
        company,
        datetime_field=True,
    )
    filters["docstatus"] = 1

    rows = frappe.get_all(
        "Work Order",
        filters=filters,
        fields=[
            "name",
            "production_item",
            "qty",
            "produced_qty",
            "status",
            "creation",
        ],
        order_by="creation desc",
        limit_page_length=20,
    )

    return _success(rows)

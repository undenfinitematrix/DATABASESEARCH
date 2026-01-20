from flask import Blueprint, request, render_template
from datetime import datetime, timedelta
import pymysql
from db_util import get_db_connection_util

apis = Blueprint("apis", __name__)

@apis.route("/ping", methods=["GET"])
def ping():
    return "API WORKING"

@apis.route('/test/aerochat-data', methods=['GET', 'POST'])  # Remove /chat from here
@apis.route('/chat/test/aerochat-data', methods=['GET', 'POST'])
def dashboard_aerochat():
    days = int(request.args.get("days") or 30)
    show_all = request.args.get("show_all") == "1"
    search = (request.args.get("search") or "").strip()

    connection = get_db_connection_util()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    query = """
        SELECT 
            uc.id AS company_id,
            uc.user_id,
            uc.brand_name,
            uc.company_email,
            uc.website_url,
            uc.brand_logo,
            uc.created_at AS company_created,
            u.last_login,
            u.country,
            up.name AS plan_name,
            up.plan_type,
            up.monthly_price,
            up.yearly_price,
            up.start_date,
            up.end_date,
            up.status,
            up.is_trail,
            un.contact_count,
            un.knowledgebase_count
        FROM user_companys AS uc
        LEFT JOIN users AS u ON u.id = uc.user_id
        LEFT JOIN user_packages AS up ON up.id = (
            SELECT id FROM user_packages
            WHERE company_id = uc.id
            ORDER BY start_date DESC
            LIMIT 1
        )
        LEFT JOIN user_numbers AS un ON un.user_id = uc.id
        WHERE 1=1
    """

    params = []

    if not show_all:
        end_date = datetime.now().replace(hour=23, minute=59, second=59)
        start_date = end_date - timedelta(days=days)
        query += " AND uc.created_at BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    if search:
        query += """
            AND (
                uc.brand_name LIKE %s OR
                uc.company_email LIKE %s OR
                uc.website_url LIKE %s OR
                u.country LIKE %s
            )
        """
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern, pattern])

    query += " ORDER BY uc.created_at DESC"

    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "aerochat_data.html",
        data=data,
        days=days,
        show_all=show_all,
        search=search,
        now=datetime.now()
    )

from __future__ import annotations

import sqlite3
from pathlib import Path


def summarize_operations_by_category_and_period(
    database_path: str | Path,
    op_type: str,
    start_date: str,
    end_date: str,
) -> list[tuple[str, float, int]]:
    """
    Параметризований SQL-запит через Python DB-API (sqlite3):
    агрегує суму (SUM) та кількість операцій (COUNT) за категоріями
    для заданого типу ('income'/'expense') і періоду дат [start_date, end_date].
    """
    with sqlite3.connect(str(database_path)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                categories.name,
                SUM(financial_operations.amount) AS total_amount,
                COUNT(financial_operations.id) AS operations_count
            FROM financial_operations
            JOIN categories
                ON financial_operations.category_id = categories.id
            WHERE financial_operations.op_type = ?
              AND financial_operations.date >= ?
              AND financial_operations.date <= ?
            GROUP BY categories.name
            ORDER BY total_amount DESC
            """,
            (op_type, start_date, end_date),
        )
        rows = cursor.fetchall()
        return [
            (str(category_name), float(total or 0.0), int(count or 0))
            for category_name, total, count in rows
        ]
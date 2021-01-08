import asyncio
import motor


async def insert_order(db, order):
    doc = await db.orders.insert_one(dict(order.__dict__))
    return doc


async def find_order(db, order_id):
    doc = await db.orders.find_one({"order_id": order_id})
    return doc if doc else None


async def drop_orders(db):
    result = await db.orders.drop()
    return result


async def insert_trade(db, trade):
    doc = await db.trades.insert_one(dict(trade.__dict__))
    return doc


async def find_trade(db, trade_id):
    doc = await db.trades.find_one({"trade_id": trade_id})
    return doc if doc else None


async def drop_trades(db):
    result = await db.trades.drop()
    return result


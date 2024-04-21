from datetime import datetime
from flask import current_app as app
from sqlalchemy.exc import SQLAlchemyError
from DB.database_connection import DatabaseConnection
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Sale(DatabaseConnection):
    __tablename__ = 'Sales'

    SaleID = Column(Integer, primary_key=True, autoincrement=True)
    VehicleID = Column(Integer, ForeignKey('Vehicles.VehicleID'), nullable=False)
    SellerUserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    BuyerUserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    SaleDate = Column(Date, nullable=False)
    SalePrice = Column(Float, nullable=False)

    vehicle = relationship("Vehicle", back_populates="sales")
    seller = relationship("User", foreign_keys=[SellerUserID])
    buyer = relationship("User", foreign_keys=[BuyerUserID])

def record_sale(vehicle_id, seller_user_id, buyer_user_id, sale_price):
    try:
        sale = Sale(
            VehicleID=vehicle_id,
            SellerUserID=seller_user_id,
            BuyerUserID=buyer_user_id,
            SaleDate=datetime.now(),
            SalePrice=sale_price
        )
        DatabaseConnection.session.add(sale)
        DatabaseConnection.session.commit()
        app.logger.info(f"Sale recorded: VehicleID={vehicle_id}, SellerUserID={seller_user_id}, BuyerUserID={buyer_user_id}, SalePrice={sale_price}")
        return True
    except SQLAlchemyError as e:
        DatabaseConnection.session.rollback()
        app.logger.error(f"Error recording sale: {e}")
        return False

def get_vehicle_sale_history(vehicle_id):
    try:
        sales = Sale.query.filter_by(VehicleID=vehicle_id).all()
        app.logger.info(f"Retrieved sale history for VehicleID={vehicle_id}")
        sales_data = [
            {"SaleID": sale.SaleID, "SaleDate": sale.SaleDate, "SalePrice": sale.SalePrice,
             "SellerUserID": sale.SellerUserID, "BuyerUserID": sale.BuyerUserID}
            for sale in sales
        ]
        return sales_data
    except SQLAlchemyError as e:
        app.logger.error(f"Error retrieving vehicle sale history for VehicleID={vehicle_id}: {e}")
        return []


def get_user_sales_statistics(user_id):
    try:
        total_sales_count = Sale.query.filter_by(SellerUserID=user_id).count()
        total_sales_value = DatabaseConnection.session.query(DatabaseConnection.func.sum(Sale.SalePrice)).filter(Sale.SellerUserID == user_id).scalar()
        app.logger.info(f"Retrieved sales statistics for UserID={user_id}: TotalCount={total_sales_count}, TotalValue={total_sales_value}")
        return {
            "total_sales_count": total_sales_count,
            "total_sales_value": total_sales_value
        }
    except SQLAlchemyError as e:
        app.logger.error(f"Error retrieving sales statistics for UserID={user_id}: {e}")
        return {}


def delete_sale(sale_id):
    try:
        sale = Sale.query.get(sale_id)
        if sale:
            DatabaseConnection.session.delete(sale)
            DatabaseConnection.session.commit()
            app.logger.info(f"Sale deleted: SaleID={sale_id}")
            return True
        else:
            app.logger.warning(f"Sale not found: SaleID={sale_id}")
        return False
    except SQLAlchemyError as e:
        DatabaseConnection.session.rollback()
        app.logger.error(f"Error deleting sale: SaleID={sale_id}, Error: {e}")
        return False

import typer

from cashier import Cashier
from constants import (
    DATABASE,
    NUM_CUSTOMERS_BEFORE_X,
    NUM_CUSTOMERS_BEFORE_Z,
    NUM_SHIFTS,
)
from customer import RandomChoiceCustomer
from store import Store

app = typer.Typer()


@app.command("list")
def pos_list() -> None:
    Store(DATABASE).print_products()


@app.command("simulate")
def pos_simulate() -> None:
    store = Store(DATABASE)
    cashier = Cashier()
    store.start_new_shift()
    while True:
        customer = RandomChoiceCustomer()
        store.new_customer()
        cart = customer.choose_items(store.get_products())
        cashier.open_receipt(store.get_customer_count())
        cashier.add_items_to_receipt(cart)
        store.print_receipt(cashier.get_receipt())
        payment = customer.choose_payment()
        cashier.close_receipt(payment)
        store.update_x(cashier.get_receipt())
        if store.get_customer_count() % NUM_CUSTOMERS_BEFORE_X == 0:
            response = typer.confirm("Do you want to make X report?")
            if response:
                store.make_x_report()

        if store.get_customer_count() % NUM_CUSTOMERS_BEFORE_Z == 0:
            response = typer.confirm("Do you want to end the shift?")
            if response:
                store.make_z_report()
                store.start_new_shift()
                if store.get_shift_count() > NUM_SHIFTS:
                    store.close_store()
                    break


@app.command("report")
def pos_report() -> None:
    Store(DATABASE).make_z_report()


if __name__ == "__main__":
    app()

# Point of Sales (POS)

## Intro

This project is a simple Point of Sales (POS) system designed to simulate a day in the life of a store with Cash Registers operating in three shifts per day. Note that UI and concurrency are out of scope for this project.

## User Stories

> As a *cashier*, I would like to open a receipt so that, I can start serving customers.

> As a *cashier*, I would like to add items to an open receipt so that, I can calculate how much the customer needs to pay.

> As a *customer*, I would like to see a receipt with all my items so that, I know how much I have to pay.

> As a *customer*, I would like to pay (by cash or card) for a receipt so that, I can receive my items.

> As a *cashier*, I would like to close the paid receipt so that, I can start serving the next customer.

> As a *store manager*, I would like to make X reports so that, I can see the current state of the store.

> As a *cashier*, I would like to make Z reports so that, I can close my shift and go home.

## Technical Details

- Store may sell items as singles
- Store may sell items as batches/packs. (think 6-pack of beer cans :D)
- Store may have discounts of various types:
  * Items may have discount
  * Batches/packs may have discount (e.g. if a customer buys a pack of tissues they get -10% off the total price)
  * Receipt may have discount based on the customer number (e.g. if the customer number is prime they get -17% off the receipt price)
- For simplicity X reports only contain revenue and count of each item sold.
- For simplicity Z report only "clears" the Cash Register. After this operation, revenue and the number of items sold (in X report) are zero.
- Persistence is handled using [SQLite](https://docs.python.org/3/library/sqlite3.html).
- The CLI is implemented using [Typer](https://typer.tiangolo.com/).


## CLI

> python -m pos list

print out information of the store such as what items do they sell, and discounts (if any).

> python -m pos simulate

Start REPL:
  - Customer with randomly selected items arrive at POS.
  - Cashier opens the receipt.
  - Cashier registers items one by one in the receipt.
  - Once the cashier registers all items, print the receipt (see example below)
  - Customer pays (picks payment method randomly)
    * with cash: print "Customer paid with cash"
    * with card: print "Customer paid with card"
  - Once the cashier confirms payment they close the receipt.

After every 20th customer, prompt the store manager if they want to make X report. A simple y/n question will suffice.
  * If they pick "y" print out X Report (see example below)
  * If they pick "n" continue the simulation

After every 100th customer, prompt the store manager if they want to end the shift. A simple y/n question will suffice.
  * If they pick "y" simulate cashier making Z Report.
  * If they pick "n" continue the simulation

After three shifts, end the simulation.

> python -m pos report

Print out information about the operation of the store. Namely,
- Sales report (item with the number)
- Revenue report (how much money the store made with each payment method)
Similar to X report but this one reports not a signle shift but the lifetime data.

## Examples

### Receipt

Product        | Units | Price |  Total  |
---------------|-------|-------|---------|
Milk           | 1     | 4.99  |  4.99   |
Mineral Water  | 6     | 3.00  |  18.00  |


### Report

Product        | Sales |
---------------|-------|
Milk           | 1     |
Bread          | 6     |
Diapers        | 2     |

Payment   | Revenue |
----------|---------|
Cash      | 40.40   |
Card      | 60.60   |


## Code Quality and Testing

The code is tested to ensure functionality and to prevent regressions(automated tests provided).
It is easy to change, following design patterns and S.O.L.I.D principles.
Linting and formatting are enforced to maintain code quality:
- Formated code using `black` auto formatter
- Sorted imports with `isort` 
- Checked static types with `mypy`
- Checked code with `flake8`
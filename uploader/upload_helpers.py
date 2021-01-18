from .models import Customer, Transaction


class ValidationError(Exception):
    __name__ = 'TransactionValidationError'


class UploadHelper:

    def __init__(self, line_data):
        self.line_data = line_data

    def parse_line_data(self):
        (c_id, c_fname, c_lname, c_street, c_state, c_zip,
         t_status, t_id, t_name, t_amount, t_time) = self.line_data

        customer = {
            # Match our id to customer id provided, rather than having 2 id's floating around for the same customer
            'id': c_id,
            'first_name': c_fname,
            'last_name': c_lname,
            'street_address': c_street,
            'state': c_street,
            'zip_code': c_zip
        }

        transaction = {
            'product_id': t_id,
            'product_name': t_name,
            'purchase_status': t_status,
            'purchase_amount': t_amount,
            'transaction_date': t_time
        }

        return customer, transaction

    def _transaction_string(self, t):
        """
        For use before creating the model, which has the str rep in it
        :return:
        """

        return (f'Transaction with product id [{t["product_id"]}]\n'
                f'{t["product_name"]} purhcased for {t["purchase_amount"]} on {t["transaction_date"]}')

    def _validate_transaction(self, t, c_id):
        simple_validations = [
            (lambda t: float(t['purchase_amount']) >= 0, f'Purchase amount {t["purchase_amount"]} is negative'),
            (lambda t: t['purchase_status'].lower() in ('new', 'canceled'),
                        f'Purchase type \'{t["purchase_status"]}\' is unrecognized')
        ]

        for err_check, err_msg in simple_validations:
            if not err_check(t):
                raise ValidationError(err_msg)


        new_purchases = Transaction.objects.filter(
                           product_id=t['product_id'],
                           customer_id=Customer.objects.get(id=c_id),
                           purchase_status='new')

        if not new_purchases and t['purchase_status'] == 'canceled':
            raise ValidationError("Cannot cancel a purchase that has not already been started")

    def upsert_customer(self, c):
        """
        If customer doesn't exist, add them. Additonally, if the customer has a new address, save the new one

        :return:
        """
        cus = Customer.objects.filter(id=c['id'])
        if not cus:
            cus = Customer.objects.create(**c)

        customer = cus.first()

        if customer.street_address != c['street_address']:
            customer.street_address = c['street_address']
            customer.state = c['state']
            customer.zip_code = c['zip_code']

            customer.save()

        # return model instance rather than queryset, filtering on id should only yield one result anyway
        return customer

    def process_transaction(self):
        """

        :return:
        """
        c, t = self.parse_line_data()

        try:
            self._validate_transaction(t, c['id'])
        except ValidationError as e:
            return (self._transaction_string(t), str(e))

        # Insert new customer if there is no entry in our db before creating the transaction
        # and linking to associated customer
        cus = self.upsert_customer(c)
        t['customer'] = cus
        Transaction.objects.create(**t)

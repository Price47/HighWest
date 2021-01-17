from .models import Customer, Transaction


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

    def _handle_new_customer_address(self, cus, c):
        if cus.street_address != c['street_address']:
            cus.street_address = c['street_address']


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
        # Insert new customer if there is no entry in our db before creating the transaction
        # and linking to associated customer
        cus = self.upsert_customer(c)
        t['customer'] = cus
        Transaction.objects.create(**t)

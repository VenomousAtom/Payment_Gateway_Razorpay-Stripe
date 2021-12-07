from flask import Flask, render_template, request, url_for, redirect
import razorpay
import stripe
# from datetime import datetime
import detes

app = Flask(__name__)

# getting the razorpay key values from the detes module
razorpay_key_id, razor_key_secret = detes.get_razorpay_details()

# Initializing the Pay Client
payClient = razorpay.Client(auth=(razorpay_key_id, razor_key_secret))

class transactions:
    transaction_reciept = 1

sess = transactions()

# getting the stripe key values from the detes module
stripe_public_key, stripe_secret_key = detes.get_stripe_details()

# setting up api key value
stripe.api_key = stripe_secret_key

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route('/razorpay/processing', methods=['POST', 'GET'])
def raz_processing():
    if request.method == 'POST':

        # Setting Up Test data for Ordering
        recp = 'Order_'+str(sess.transaction_reciept)
        order_data = {
            # 100 Rupees should listed as 100*100 Paisa (Smallest Amount in Currency)
            "amount": 12599*100,
            "currency": "INR",
            "receipt": recp,
        }

        # Sending Order Data to the Server to initialise an Order and Retrieve an Order ID
        Order = payClient.order.create(data=order_data)
        order_id = Order['id']

        sess.transaction_reciept += 1

        return render_template(
            'razorpay-processing.html',
            keyid=razorpay_key_id,
            orderid=order_id
        )

    else:
        return "Unauthorized!!!"

@app.route('/razorpay/verification', methods=['POST', 'GET'])
def raz_verify():
    if request.method == 'POST':
        try:
            # Get the Relevant Information from Form to verify Payment
            payid = request.form.get("paymentid")
            ordid = request.form.get("orderid")
            sign = request.form.get("signature")

            # Verify Payment
            payClient.utility.verify_payment_signature(
                {
                    "razorpay_payment_id": payid,
                    "razorpay_order_id": ordid,
                    "razorpay_signature": sign
                }
            )
            return render_template("success.html")
        except:
            return render_template("fail.html")
    else:
        return "Unauthorized!!!"

@app.route('/stripe/processing', methods=['POST', 'GET'])
def str_processing():
    # Set a Checkout Session for Stripe
    session = stripe.checkout.Session.create(
        # Set Payment Methods
        payment_method_types=['card'],
        # Payment Line Items
        line_items=[{
            'price': "price_1K401GSBJs8AvQrd5YDvv5S2", #Product Price API ID
            'quantity': 1,
        }],
        mode='payment',
        # Payment Successful Redirect URL
        success_url= url_for('str_success', _external=True),

        # Payment Failure Redirect URL
        cancel_url= url_for('str_fail', _external=True),
    )

    # session.url redirects to the Sessions Checkout Page
    return redirect(session.url, code=303)
    # render_template(
    #     'stripe-processing.html',
    #     checkout_session_id=session['id'],
    #     checkout_public_key=stripe_public_key
    # )

@app.route('/stripe/success')
def str_success():
    return render_template('success.html')

@app.route('/stripe/fail')
def str_fail():
    return render_template('fail.html')

if __name__ == "__main__":
    app.run(debug=True)

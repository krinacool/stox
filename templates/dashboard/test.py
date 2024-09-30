import hashlib
import random
import time
import uuid

userid = 'itoyiho'
amount = '100'
MERCHANT_KEY = "QQjxu1"
SALT = "JQrrQBzBX00C2Ogeb509nnb1r0zDbCfr"

# Generate the txnid similarly to the PHP logic
txnid = "TXNKAD" + str(random.randint(0, 1000)) + "_" + userid

productInfo = "Txn For Product #1122"
firstname = "User_" + uuid.uuid4().hex
email = "onlineservice1542@gmail.com"
phone = "9865452575"

# Create the hash_string exactly as in PHP
hash_string = f"{MERCHANT_KEY}|{txnid}|{amount}|{productInfo}|{firstname}|{email}|{userid}||||||||||{SALT}"

# Generate the hash using SHA-512 and convert to lowercase
hash_value = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()

# Print the redirection message
print('<h1 style="color:red;text-align:center;">Please Wait We are redirecting you on Payment Page</h1>')

# Generate the HTML form for redirection
html_form = f"""
<body>
<form action="https://secure.payu.in/_payment" method="post" name="payuForm">
      <input type="hidden" name="key" value="{MERCHANT_KEY}" />
     <input type="hidden" name="hash" value="{hash_value}"/>
     <input type="hidden" name="txnid" value="{txnid}" />
    <input type="hidden" name="amount" value="{amount}">
    <input type="hidden" name="productinfo" value="{productInfo}">
    
    <input type="hidden" name="firstname" value="{firstname}">
    <input type="hidden" name="email" value="{email}">
    <input type="hidden" name="phone" value="{phone}">
    <input type="hidden" name="mobile" value="{phone}">
    <input type="hidden" name="surl" value="https://crsorgi-gob.in/web/index.php/auth/dashboard/payments/payu/pgResponse.php">
    <input type="hidden" name="furl" value="https://crsorgi-gob.in/web/index.php/auth/dashboard/wallet.php">
    <input type="hidden" name="udf1" value="{userid}">
     
    <input type="hidden" name="service_provider" value="payu_paisa" size="64" />
    <script>
    document.body.onload = function(ev){{
         document.payuForm.submit();
    }}
    </script>
</form>
</body>
"""

# Output the HTML form
print(html_form)

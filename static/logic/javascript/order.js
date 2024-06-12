
function getSymbol(symbol) {
    if (symbol.includes('SENSEX')) {
        return 'SENSEX';
    }
    var match = symbol.match(/(.*?)(\d{2}[A-Z]{3}\d+)/);
    if (match) {
        var result = match[1];
        return result;
    } else {
        return symbol;
    }
}

function option_lot(symbol) {
    console.log('OPTION LOT')
    option_chain = document.getElementById('option_chain').getAttribute('data-chain')
    option_chain = JSON.parse(option_chain)
    gets = getSymbol(symbol)
    if(gets in option_chain){
        document.getElementById('quantity_label').innerHTML = `<span>Lot</span><span class="quantity_lot">Quantity : <span id='lot_quantity' class="lotsize" style="min-width: 60px;"> ${option_chain[gets]}</span></span>`
    }
    else {
        document.getElementById('quantity_label').innerHTML = `Quantity`
    }
}


function transact() {
    console.log('Hello, World !')
    // PLACING ORDER
    let csrf = $("input[name=csrfmiddlewaretoken]").val()
    let instrument = $("input[name=instrument]").val()
    let token = $("input[name=token]").val()
    let symbol = $("input[name=symbol]").val()
    let price = $("input[name=price]").val()
    let quantity = $("input[name=quantity]").val()
    let order_type = $("input[name=order_type]").val()
    let product = $("input[name=product]").val()
    let type = $("input[name=type]").val()
    let stoploss = $("input[name=stoploss]").val()
    let target = $("input[name=target]").val()
    if(symbol.trim() == '' || price.trim() == ''|| quantity.trim() == '' || order_type.trim() == '' || product.trim() == '' || type.trim() == '')
    {
        console.log('Present')
        document.getElementById('alert').classList.remove('display-none');
        document.getElementById('alert').classList.add('alert-danger');
        document.getElementById('alert').classList.remove('alert-success');
        document.getElementById('alert').innerHTML = "Invalid Order Details"
        return false
    }
    document.getElementById('alert').classList.remove('display-none');
    document.getElementById('alert').classList.remove('alert-danger');
    document.getElementById('alert').classList.add('alert-success');
    document.getElementById('alert').innerHTML = "Order executed Successfully !";
    document.getElementById('order_cancel').click()
    mydata = { symbol: symbol, price: price, quantity: quantity, order_type: order_type, product:product, type:type, stoploss:stoploss, target:target,instrument:instrument,token:token ,csrfmiddlewaretoken: csrf }
    $.ajax({
        url: "/async_transact",
        method: "POST",
        data: mydata,
        success: function (data) {
            if (data['success']){
                document.getElementById('alert').classList.remove('alert-danger');
                document.getElementById('alert').classList.add('alert-success');
            }
            else {
                document.getElementById('alert').classList.add('alert-danger');
                document.getElementById('alert').classList.remove('alert-success');
            }
            document.getElementById('alert').classList.remove('display-none');
            document.getElementById('alert').innerHTML = data['message'];
        },
    });
}


function order(data) {
    let symbol = $(data).data('symbol')
    option_lot(symbol)
    let token = $(data).data('token')
    console.log('token')
    console.log(token)
    let instrument = $(data).data('instrument')
    let info = document.getElementById(`${instrument}price`)
    let open = info.getAttribute('data-open')
    let high = info.getAttribute('data-high')
    let low = info.getAttribute('data-low')
    let close = info.getAttribute('data-close')
    let price = info.getAttribute('data-price')
    document.getElementById('order_tab').classList.toggle('show')
    document.getElementById('order_tab_form').action = `/transact`
    document.getElementById('order_tab_symbol').innerHTML = symbol
    document.getElementById('delete_symbol').innerHTML = `
    <a href="/delete_symbol/${symbol}"></a>
    `
    document.getElementById('order_tab_symbolinput').value = symbol
    document.getElementById('order_tab_priceinput').innerHTML = price
    document.getElementById('order_tab_priceinput').value = price
    document.getElementById('order_tab_tokeninput').value = token
    document.getElementById('order_tab_instrumentinput').value = instrument
    calculate_margin()
    document.getElementById('order_tab_info').innerHTML = `<div class="col-3">
    <p class="text-center text-muted m-b-10">Open</p>
    <p class="text-center text-dark m-b-10"><b>${open}</b></p>
</div>
<div class="col-3">
    <p class="text-center text-muted m-b-10">High</p>
    <p class="text-center text-dark m-b-10"><b>${high}</b></p>
</div>
<div class="col-3">
    <p class="text-center text-muted m-b-10">Low</p>
    <p class="text-center text-dark m-b-10"><b>${low}</b></p>
</div>
<div class="col-3">
    <p class="text-center text-muted m-b-10">Close</p>
    <p class="text-center text-dark m-b-10"><b>${close}</b></p>
</div>`
}
document.getElementById('order_tab_intraday').addEventListener('click', event => {
    document.getElementById('order_tab_product').value = 'INTRADAY'
    document.getElementById('order_tab_carryforward').classList.remove('btn-dark')
    document.getElementById('order_tab_carryforward').classList.add('btn-outline-dark')
    document.getElementById('order_tab_intraday').classList.add('btn-dark')
    document.getElementById('order_tab_intraday').classList.remove('btn-outline-dark')
    calculate_margin()
})

document.getElementById('order_tab_carryforward').addEventListener('click', event => {
    document.getElementById('order_tab_product').value = 'CARRYFORWARD'
    document.getElementById('order_tab_carryforward').classList.add('btn-dark')
    document.getElementById('order_tab_carryforward').classList.remove('btn-outline-dark')
    document.getElementById('order_tab_intraday').classList.remove('btn-dark')
    document.getElementById('order_tab_intraday').classList.add('btn-outline-dark')
    calculate_margin()
})

document.getElementById('order_tab_market').addEventListener('click', event => {
    document.getElementById('order_tab_type').value = 'MARKET'
    document.getElementById('order_tab_priceinput').setAttribute("readonly", "True");
    document.getElementById('order_tab_priceinput').classList.add('market_price')
    document.getElementById('order_tab_limit').classList.remove('btn-dark')
    document.getElementById('order_tab_limit').classList.add('btn-outline-dark')
    document.getElementById('order_tab_market').classList.add('btn-dark')
    document.getElementById('order_tab_market').classList.remove('btn-outline-dark')
})

document.getElementById('order_tab_limit').addEventListener('click', event => {
    document.getElementById('order_tab_type').value = 'LIMIT'
    document.getElementById('order_tab_priceinput').removeAttribute("readonly", "True");
    document.getElementById('order_tab_priceinput').classList.remove('market_price');
    document.getElementById('order_tab_limit').classList.add('btn-dark')
    document.getElementById('order_tab_limit').classList.remove('btn-outline-dark')
    document.getElementById('order_tab_market').classList.remove('btn-dark')
    document.getElementById('order_tab_market').classList.add('btn-outline-dark')
})

document.getElementById('order_tab_buy').addEventListener('click', event => {
    document.getElementById('order_tab_ordertypeinput').value = 'BUY'
    transact()
    // document.getElementById('order_tab_form').submit()
})

document.getElementById('order_tab_sell').addEventListener('click', event => {
    document.getElementById('order_tab_ordertypeinput').value = 'SELL'
    transact()
    // document.getElementById('order_tab_form').submit()
})

function calculate_margin() {
    let symbol = document.getElementById('order_tab_symbolinput').value
    let quantity = document.getElementById('order_tab_quantity').value
    let product = document.getElementById('order_tab_product').value
    let price = document.getElementById('order_tab_priceinput').value
    let wallet = document.getElementById('wallet').getAttribute('data-wallet')
    let margin = document.getElementById('wallet').getAttribute('data-margin')
    let charges = document.getElementById('wallet').getAttribute('data-charges')
    let tax = document.getElementById('wallet').getAttribute('data-tax')
    gets = getSymbol(symbol)
    if(gets in option_chain){
        quantity = quantity*option_chain[gets]
        document.getElementById('lot_quantity').innerHTML = `${quantity}`
    }
    else {
        document.getElementById('quantity_label').innerHTML = `Quantity`
    }
    let total = quantity * price
    
    cls = ""
    if (product == 'INTRADAY'){
        if (total < wallet * margin) {
            cls = 'text-success'
        }
        else {
            cls = 'text-danger'
        }
        document.getElementById('wallet').innerHTML = wallet*margin
    }
    else {
        if (total < wallet) {
            cls = 'text-success'
        }
        else {
            cls = 'text-danger'
        }
        document.getElementById('wallet').innerHTML = wallet
    }
    document.getElementById('margin_required').innerHTML = `
    <details>
    <summary>
    <span class="${cls}">${(total).toFixed(2)}</span> + 
    <span class="text-info">Charges</span></summary>
    Onstock Brokerage : ${charges}
    <br>
    Taxes : ${((tax / 100) * total).toFixed(2)}
     </details>
    `
}

function smart_order() {
    // document.getElementById('smart_order_button').classList.add('display-none');
    document.getElementById('smart_order').classList.remove('display-none');
    location.href = '#smart_order'
}


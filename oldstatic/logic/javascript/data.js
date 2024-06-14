function updating() {
    const apiUrl = `http://127.0.0.1:8000/update_data`;
    let thisline = ""
    fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => {
            a = data
            for (let i of data['symbollist']) {
                try {
                    let lines = ""
                    let value = data[i];
                    console.log(value)
                    let change = (value.ltp - value.close).toFixed(2);
                    let cls = "";
                    if (change > 0) {
                        cls = "text-c-green"
                    }
                    else {
                        cls = "text-c-red"
                    }
                    thisline = `<h6 id="${i}price" data-price="${value.ltp}" data-open="${value.open}" data-close="${value.close}" data-high="${value.high}" data-low="${value.low}">${value.ltp}</h6>
                <p class="${cls}">${change}</p>`
                    lines = lines + thisline
                    document.getElementById(i).innerHTML = lines
                }
                catch { }
            }
        })
        .catch((error) => console.log(error));

}
setInterval(updating, 1000);
// updating()
function updating() {
    const apiUrl = `https://onstock.in/update_data`;
    let thisline = ""
    let lines = ""
    fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => {
            a = data
            for (let i of data['symbollist']) {
                let value = data[i];
                let change = (value.currentPrice - value.previousClose).toFixed(2);
                let cls = "";
                if (change>0) {
                    cls = "text-c-green"
                }
                else {
                    cls = "text-c-red"
                }
                thisline = `<tr class="unread">
            <td>
                <a data-toggle="collapse" href="#${i}" role="button" aria-expanded="false"
                    aria-controls="${i}">
                    <h6>${i}</h6>
                    <p>NSE</p>
                </a>
            </td>
            <td>
                <h6>${value.currentPrice}</h6>
                <p class="${cls}">${change}</p>
            </td>
        </tr>
        <tr class="collapse" id="${i}">
            <td>
                Previous close : ${value.previousClose}
            </td>
        </tr>`
                lines = lines + thisline
            }
            document.getElementById("table_body").innerHTML = lines
        })
        .catch((error) => console.log(error));
}
setInterval(updating, 1000);
// updating()
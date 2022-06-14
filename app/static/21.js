const hit = document.getElementById("hit");
const stand = document.getElementById("stand");
const reset = document.getElementById("reset");

let next_name = "";

function call_stand(){
    axios({
        method: "GET",
        url: api.stand
    }).then((resp) => {
        if(resp.data.game == "end"){
            document.getElementById("your_hand").innerHTML = "";
            resp.data.you.hand.forEach((card) => {
                let img = document.createElement("img");
                img.setAttribute("src", cards[card.src]);
                img.setAttribute("alt", card.alt);

                document.getElementById("your_hand").appendChild(document.createTextNode(" "));
                document.getElementById("your_hand").appendChild(img);
            });

            document.getElementById("winning_rate_text").innerText=resp.data.count.winning_rate + "%";

            document.getElementById("your_total").innerText = resp.data.you.total;

            document.getElementById("statusHead").setAttribute("style", `color:${resp.data.alert.color}`);
            document.getElementById("statusHead").innerText = resp.data.alert.head;
            document.getElementById("statusBody").innerHTML = resp.data.alert.body;

            document.getElementById("game-total").innerText = resp.data.count.total;
            document.getElementById("game-win").innerText = resp.data.count.win;
            document.getElementById("game-rate").innerText = resp.data.count.winning_rate + "%";

            next_name = resp.data.name.you;

            document.body.classList.add("is-clipped");
            document.getElementById("showGameStatus").classList.add("is-active");

            reset.focus();
        }
        else if(resp.data.game == "not found"){
            location.reload();
        }
    }).catch((err) => {
        console.log(err);
        window.alert("오류가 발생했습니다. 버튼을 다시 눌러주십시오.");
    });
}

hit.addEventListener("click", () => {
    axios({
        method: "GET",
        url: api.hit
    }).then((resp) => {
        if(resp.data.game == "ok"){
            if(resp.data.you){
                let img = document.createElement("img");
                img.setAttribute("src", cards['back']);
                img.setAttribute("alt", "Hidden Card");

                document.getElementById("your_hand").appendChild(document.createTextNode(" "));
                document.getElementById("your_hand").appendChild(img);

                // cant check your total
            }

            let me = document.createElement("img");
            me.setAttribute("src", cards[resp.data.me.src]);
            me.setAttribute("alt", resp.data.me.alt);
            document.getElementById("my_hand").appendChild(document.createTextNode(" "));
            document.getElementById("my_hand").appendChild(me);

            document.getElementById("my_total").innerText = resp.data.me.total;
        }
        else if(resp.data.game == "not found"){
            location.reload();
        }
        else if(resp.data.game == "bust"){
            call_stand();
        }
        else if(resp.data.game == "bust with new card"){
            let me = document.createElement("img");
            me.setAttribute("src", cards[resp.data.me.src]);
            me.setAttribute("alt", resp.data.me.alt);

            document.getElementById("my_hand").appendChild(document.createTextNode(" "));
            document.getElementById("my_hand").appendChild(me);

            document.getElementById("my_total").innerText = resp.data.me.total;

            call_stand();
        }
    }).catch((err) => {
        console.log(err);
        window.alert("오류가 발생했습니다. 버튼을 다시 눌러주십시오.");
    });
});
stand.addEventListener("click", call_stand);

reset.addEventListener("click", function(){
    axios({
        method: "GET",
        url: api.status,
    }).then((resp) => {
        document.getElementById("your_total").innerText = resp.data.you.total;
        document.getElementById("your_hand").innerHTML = "";
        resp.data.you.hand.forEach((card) => {
            let img = document.createElement("img");
            img.setAttribute("src", cards[card.src]);
            img.setAttribute("alt", card.alt);

            document.getElementById("your_hand").appendChild(document.createTextNode(" "));
            document.getElementById("your_hand").appendChild(img);
        });

        document.getElementById("my_total").innerText = resp.data.me.total;
        document.getElementById("my_hand").innerHTML = "";
        resp.data.me.hand.forEach((card) => {
            let img = document.createElement("img");
            img.setAttribute("src", cards[card.src]);
            img.setAttribute("alt", card.alt);

            document.getElementById("my_hand").appendChild(document.createTextNode(" "));
            document.getElementById("my_hand").appendChild(img);
        });

        document.body.classList.remove("is-clipped");
        document.getElementById("showGameStatus").classList.remove("is-active");

        if(next_name.length != 0)
            document.getElementById("you-name").innerText = next_name;
    }).catch((err) => {
        console.log(err);
        location.reload();
    });
});

document.addEventListener('keydown', (key) => {
    key = key.key.toLowerCase();
    if(document.getElementById("showGameStatus").classList.contains("is-active")){
        reset.click();
    } else {
        if(key == 'h'){
            hit.click();
        } else if(key == 's') {
            stand.click();
        }    
    }
});
const hit = document.getElementById("hit");
const stand = document.getElementById("stand");
const reset = document.getElementById("reset");

let next_name = "";

function get_card_img(owner, card_id, alt){
    let img = document.createElement("img");
    img.setAttribute("src", cards[card_id]);
    img.setAttribute("alt", alt);
    img.addEventListener('click', card_on_click);
    img.setAttribute("data-id", card_id);
    img.setAttribute("data-owner", owner);

    return img;
}

function get_hand(target){
    if(target == "me"){
        return document.getElementById("my_hand");
    } else if (target == "you") {
        return document.getElementById("your_hand");
    } else {
        throw new Error(`target must be 'you' or 'me' not ${target}`)
    }
}

function appendCard(owner, card){
    let hand = get_hand(owner);
    hand.appendChild(document.createTextNode(" "));
    hand.appendChild(get_card_img(owner, card.src, card.alt));
}

function card_on_click(event){
    if(event.target.dataset.owner === "me" && event.target.dataset.id === "joker"){
        if(confirm("조커 카드를 패에서 버릴까요?")){
            axios({
                method: "GET",
                url: api.joker
            }).then((resp) => {
                if(resp.data.game == "ok"){
                    if(resp.data.joker === true){
                        event.target.remove();
                        document.getElementById("my_total").innerText = resp.data.total;

                        alert("버렸습니다!");
                    } else {
                        location.reload();
                    }
                }
            }).catch((err) => {
                console.log(err);
                window.alert("오류가 발생했습니다. 버튼을 다시 눌러주십시오.");
            });
        }
    }
}

function call_stand(){
    axios({
        method: "GET",
        url: api.stand
    }).then((resp) => {
        if(resp.data.game == "end"){
            document.getElementById("your_hand").innerHTML = "";
            resp.data.you.hand.forEach((card) => appendCard("you", card));

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
                appendCard("you", {src: "back", alt: "Hidden Card"});
                // cant check total
            }

            appendCard("me", resp.data.me);
            document.getElementById("my_total").innerText = resp.data.me.total;
        }
        else if(resp.data.game == "not found"){
            location.reload();
        }
        else if(resp.data.game == "bust"){
            call_stand();
        }
        else if(resp.data.game == "bust with new card"){
            appendCard("me", resp.data.me);
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
        resp.data.you.hand.forEach((card) => appendCard("you", card));

        document.getElementById("my_total").innerText = resp.data.me.total;
        document.getElementById("my_hand").innerHTML = "";
        resp.data.me.hand.forEach((card) => appendCard("me", card));

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
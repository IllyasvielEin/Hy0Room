// template for chatPost
const template = Handlebars.compile(document.querySelector('#chatPost').innerHTML);

window.onload = function(){
    const msgArea = document.getElementById("msg");
    msgArea.addEventListener('keypress', evt => {
        if (evt.key === 'Enter' && evt.shiftKey) {
            evt.preventDefault()
            document.querySelector('#send').click();
        }
    });
};

document.addEventListener('DOMContentLoaded', () => {
    /* connect to socket */
    let socket = io.connect(location.protocol + "//" + document.location.host);

    socket.on('connect', () => {
        socket.emit('join', {room: cur_channel_id});

        document.querySelector("#send").onclick = () => {
            const msg = document.querySelector('#msg').value;
            const post_time = new Date();
            // console.log(msg);
            socket.emit('send msg', {
                'user_id': cur_user_id,
                'username': encodeURI(cur_user_name),
                'send_at': post_time,
                'content': encodeURI(msg),
                'channel_id': encodeURI(cur_channel_id)});
        };
    });

    socket.on('emit msg', data => {
        // console.log('emit msg: ' + JSON.stringify(data));
        if (cur_channel_id === data.channel_id) {
            const postTime = new Date(data.send_at);
            const content = template(
                {
                    'mes_id': data.mes_id,
                    'username': decodeURI(data.username),
                    'send_at': format_date(postTime),
                    'content': decodeURI(data.content),
                    'same_user': decodeURI(data.user_id)===cur_user_id
                }
            );
            document.querySelector("#msgTbl").innerHTML += content;
            document.querySelector("#msg").value = '';
            /* scroll to the page bottom */
            window.scrollTo(0, document.body.scrollHeight);
        }
    });

    socket.on('recall msg', data => {
        // console.log('recall msg: ' + JSON.stringify(data));
        const mes_id = data['mes_data_id'];
        const elem = document.querySelector('[data-mes-id="' + mes_id + '"]');
        if (elem) {
            elem.innerText = '原消息已撤销';
            elem.style.color = 'grey';
        }
        else {
            // console.log('null elem')
        }
    });

    socket.on('disconnect', function() {
        socket.emit('leave', {room: cur_channel_id});
    })
});

document.addEventListener("click", evt => {
    let socket = io.connect(location.protocol + "//" + document.location.host);
    const tgt = evt.target;
    if (tgt.dataset.class === 'del'){
        const elem = tgt.parentElement.parentElement.querySelector('[data-class="content"]');;
        elem.innerText = '原消息已撤销';
        elem.style.color = 'grey';
        // console.log(encodeURI(cur_channel_id) + ': ' + tgt.dataset.id);
        socket.emit("del msg",
            {
                'channel': encodeURI(cur_channel_id),
                'id': tgt.dataset.id
            }
        );
    }
});

function format_chats(messages, userId=cur_user_id){
    /* json_data is a dict */
    let output = '';
    messages.forEach(function(message) {
        const rslt_date = new Date(message.send_at)
        const rslt = template(
            {
                'mes_id': message.id,
                'user_id': message.user_id,
                'username': decodeURI(message.username),
                'send_at': format_date(rslt_date),
                'content': decodeURI(message.content),
                'same_user': decodeURI(message.user_id) === userId
            }
        );
        output += rslt
    });
    return output;
}

function format_date(date){
    const yr = date.getFullYear();
    const mo = date.getMonth() + 1;
    const dt = date.getDate();
    const hr = date.getHours();
    const mi = date.getMinutes();
    const se = date.getSeconds();
    const ms = date.getMinutes();
    return yr + "-" + lead_zero(mo) + "-" + lead_zero(dt) + " " +
        lead_zero(hr) + ":" + lead_zero(mi) + ":" + lead_zero(se) +
        "." + lead_zero(ms, 3);
}

function lead_zero(num, digits=2){
    /* put zeros in front the num */
    return (Array(digits).join("0") + num).slice(-digits);
}

// function format_tz_offset(offset_min){
//     const sign = (offset_min < 0) ? '+' : '-';
//     const hr = Math.abs(offset_min) / 60;
//     const mi = Math.abs(offset_min) % 60;
//     return sign + lead_zero(hr) + ":" + lead_zero(mi);
// };
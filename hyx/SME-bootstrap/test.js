document.body.onload = function() {
    side_bar_pos();
}
document.body.onscroll = function() {
    side_bar_pos();
}

function side_bar_pos() {
    if (window.screen.width > 1200) {
        var pos = document.body.scrollTop + document.documentElement.scrollTop; //页面被卷起来的高度
        var top_play_div_height = document.getElementById("top_play_div").offsetHeight;
        if (pos >= top_play_div_height) { //滚动到导航栏初始位置以下
            var innerHeight = window.innerHeight; //窗口可视区域高度
            var body_height = document.body.scrollHeight; //整个页面高度
            var footer_height = document.getElementById("footer").offsetHeight;
            var side_bar_height = document.getElementById("side_bar").offsetHeight;
            //页面被卷高度+side_bar高度+顶部nav高度>页面高度-footer高度
            //即side_bar底部接触footer顶部
            if (Number(pos) + Number(side_bar_height) + Number(70) > Number(body_height) - Number(footer_height)) {
                //接近页面底部
                document.getElementById('side_bar').style.position = "relative";
                var main_content_height = document.getElementById("main_content").offsetHeight;
                var res = main_content_height - side_bar_height;
                //这20px是#main_content的padding带来的
                document.getElementById('side_bar').style.top = res + "px";
            } else { //随页面滚动
                var res = pos - top_play_div_height;
                document.getElementById('side_bar').style.position = "relative";
                document.getElementById('side_bar').style.top = res + "px";
            }
        } else { //保持原位置
            document.getElementById('side_bar').style.position = "static";
            document.getElementById('side_bar').style.top = "0";
        }
    } else { //保证从PC常规视图切换到移动端模拟器时,导航栏的位置正确
        document.getElementById('side_bar').style.position = "static";
        document.getElementById('side_bar').style.top = "0";
    }
}

function click_to_read(li_id) {
    if (window.screen.width > 1000) {
        var top_play_div_height = document.getElementById("top_play_div").offsetHeight;
        window.scrollTo(0, top_play_div_height);
    } else {
        var top_play_div_height = document.getElementById("top_play_div").offsetHeight;
        var side_bar_height = document.getElementById("side_bar").offsetHeight;
        window.scrollTo(0, top_play_div_height + side_bar_height);
    }

    //更改样式
    for (var i = 1; i <= 8; i++) {
        var id = "sm" + i;
        document.getElementById(id).className = "unclicked";
        id = "sm" + i + "a";
        document.getElementById(id).className = "unclicked";

    }
    for (var i = 1; i <= 2; i++) {
        id = "bg" + i;
        document.getElementById(id).className = "unclicked";
        id = "bg" + i + "a";
        document.getElementById(id).className = "unclicked";
    }
    /*document.getElementById(li_id).className = "clicked";
    id = li_id + "a";
    document.getElementById(id).className = "clicked";*/
}
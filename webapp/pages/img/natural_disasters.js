
window.onload = function(){
    var a = document.getElementsByClassName("words_for_pics");
    for(var i=0;i<a.length;i++){
        a[i].style.display = "block";
    }
}


var scrollHeight = document.body.scrollHeight;
var height = window.innerHeight;
var scroll = document.getElementsByClassName("scroll")[0];

window.onscroll=function(){
　　var t =document.documentElement.scrollTop||document.body.scrollTop; //变量t就是滚动条滚动时，到顶部的距离
    if(scrollHeight-4<height+t){
        scroll.style.display = "none"
    }
    else{
        scroll.style.display = "block"
    }
}

window.onresize =function(){
    height = window.innerHeight;
}


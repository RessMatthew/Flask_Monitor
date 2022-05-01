
function init(){
    var resourcesPaths = `${resourcesPath}`;
    var backImageNames = `${backImageName}`;
    var modelDirString = `${modelDir}`;
    var modelDirs = modelDirString.split(',');

    initDefine(resourcesPaths, backImageNames, modelDirs);
}

// 监听复制
(function() {
    document.addEventListener('copy',(e)=>{
      e.preventDefault();
      e.stopPropagation();
      showMessage('你都复制了些什么呀,能让我看看吗？', 5000, true)
    })
  }());


function showMessage(text, timeout, flag){
    if(flag || sessionStorage.getItem('waifu-text') === '' || sessionStorage.getItem('waifu-text') === null){
        if(Array.isArray(text)) text = text[Math.floor(Math.random() * text.length + 1)-1];
        //console.log(text);
        if(flag) sessionStorage.setItem('waifu-text', text);
        $('.live2d-tips').stop();
        $('.live2d-tips').html(text).fadeTo(200, 1);
        if (timeout === undefined) timeout = 5000;
        hideMessage(timeout);
    }
}

function hideMessage(timeout){
    $('.live2d-tips').stop().css('opacity',1);
    if (timeout === undefined) timeout = 5000;
    window.setTimeout(function() {sessionStorage.removeItem('waifu-text')}, timeout);
    $('.live2d-tips').delay(timeout).fadeTo(200, 0);
}

// 工具栏的点击事件
$('.tool .fui-home').click(function (){
  showMessage('今天的天气是14℃，有些冷，记得增添衣物哦', 5000, true)
});

$('.tool .fui-eye').click(function (){
  showMessage('2', 5000, true)
});

$('.tool .fui-chat').click(function (){
  showMessage('3', 5000, true)
});

$('.tool .fui-user').click(function (){
  showMessage('4', 5000, true)
});

$('.tool .fui-info-circle').click(function (){
  showMessage('5', 5000, true)
});

$('.tool .fui-cross').click(function (){
    showMessage('6', 5000, true)
});

$('.tool .fui-photo').click(function (){
    showMessage('7', 5000, true)
});
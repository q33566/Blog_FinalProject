$(window).on('load', function () {
    waterfall();
    //模拟后台数据
    var dataInt = { "data": [{ "src": "1.jpg" }, { "src": "2.jpg" }, { "src": "3.jpg" }] }
    $(window).on('scroll', function () {
        if (checkScrollSlide) {
            // 遍历后台的数据
            $.each(dataInt.data, function (key, value) {
                // 直接用jQuery方法就可以创建元素，添加类名，添加到父元素后面，方法可以通过.迭代 
                var oBox = $('<div>').addClass('box').appendTo('#main');
                var oPic = $('<div>').addClass('pic').appendTo($(oBox));
                var oImg = $('<img>').attr('src', 'img/' + $(value).attr('src')).appendTo($(oPic));
            })
            waterfall();
        }
    })
})

function waterfall() {
    //包含选择器， 空格选择器会选择所有的子元素
    // > 取mian元素的第一个子元素
    var $boxs = $('#main>div');
    // 列宽  width（）只能获得图片的宽度，
    // outerWidth（）能获得包括边界的宽度
    var w = $boxs.eq(0).outerWidth();
    var cols = Math.floor($(window).width() / w);
    $('#main').width(cols * w).css('margin', '0 auto');
    var hArr = [];
    // jquery的遍历方法
    $boxs.each(function (index, value) {
        //console.log(value); 打印的是dom对象，
        // 获取每个图片的高
        var h = $boxs.eq(index).outerHeight();
        if (index < cols) {
            // 获取第一行的高度
            hArr[index] = h;
        }
        else {
            // 获取最矮的图片的索引
            var minH = Math.min.apply(null, hArr);
            // inArray函数能获取指定数值的索引
            var minHIndex = $.inArray(minH, hArr);
            // value是dom对象，不能直接用jQuery方法直接操作
            // 要转换为jQuery对象
            $(value).css({
                'position': 'absolute',
                'top': minH + 'px',
                'left': minHIndex * w + 'px'
            })
            // 在else循环中  改变的是加上下一行元素后的高度
            hArr[minHIndex] += $boxs.eq(index).outerHeight();
        }
    })
    //console.log(hArr);
}

function checkScrollSlide() {
    // 获取最后一个图片
    var $lastBox = $('main>div').last();
    // 最后一个图片距离父元素的高度和自身一半的高度
    var lastBoxDis = $lastBox.offset().height + Math.floor($lastBox.outerHeight());
    // 划过的高度
    var scrollTop = $(window).scrollTop();
    // 浏览器的高度
    var documentH = $(window).height();
    return (lastBoxDis < scrollTop + documentH) ? true : false;
}
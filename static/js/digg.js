function change_like(obj, content_type, object_id) {
        // 判断obj中是否包含active的元素，用于判断当前状态是否为激活状态
        var is_like = $(obj).hasClass('active') == 0
        console.log(is_like)
        $.ajax({
            url: '/digg/',
            // 为了避免加入csrf_token令牌，所以使用GET请求
            type: 'GET',
            // 返回的数据用于创建一个点赞记录
            data: {
                content_type: content_type,
                article_id: object_id,
                is_like: is_like,
            },
            cache: false,
            success: function (data) {

                // 更新点赞状态
                // 通过class找到对应的标签
                var record = $(document.getElementById('like'+ object_id))
                var bu = document.getElementById('like'+ object_id)
                if (data == '1'){
                    record.addClass('active')
                    bu.setAttribute("disabled", true)
                    bu.innerHTML = 'like success'
                }
                else if(data == '2') {
                    record.removeClass('active')
                    bu.setAttribute("disabled", true)
                    bu.innerHTML = 'repetition'
                }
                else{
                    record.removeClass('active')
                    bu.disable = false
                    bu.innerHTML = 'try again'
                }
            },
            error: function (xhr) {
                console.log(0)
            }
        });
        return false;
    };
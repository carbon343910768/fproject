function change_delete(obj, content_type, object_id) {
        // 判断obj中是否包含active的元素，用于判断当前状态是否为激活状态
        var is_delete = $(obj).hasClass('active') == 0
        console.log(is_delete)
        $.ajax({
            url: '/delete/',
            // 为了避免加入csrf_token令牌，所以使用GET请求
            type: 'GET',
            // 返回的数据用于创建一个点赞记录
            data: {
                content_type: content_type,
                article_id: object_id,
                is_delete: is_delete,
            },
            cache: false,
            success: function (data) {

                // 更新点赞状态
                // 通过class找到对应的标签
                var bu = document.getElementById('blog'+ object_id)
                if (data == '1'){
                    bu.parentNode.removeChild(bu);
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
$('#mytab').bootstrapTable({
        {#全部参数#}
        //请求后台的URL（*）或者外部json文件，json内容若为json数组[{"id": 0,"name": "Item 0","price": "$0"},{"id": 1,"name": "Item 1","price": "$1"}]，
        //且键的名字必须与下方columns的field值一样，同时sidePagination需要设置为client或者直接注释掉，这样前台才能读取到数据，且分页正常。
        //当json文件内容为json对象时：{"total": 2,"rows": [{"id": 0,"name": "Item 0","price": "$0"},{"id": 1,"name": "Item 1","price": "$1"}]}，
        //分页要写为server，但是server如果没有处理的话,会在第一页显示所有的数据，分页插件不会起作用
        {#url: "{% static 'guchen_obj.json' %}",     #}

        url:"/getdata",     //从后台获取数据时，可以是json数组，也可以是json对象
        dataType: "json",
        method: 'get',                      //请求方式（*）
        toolbar: '#toolbar',                //工具按钮用哪个容器
        striped: true,                      //是否显示行间隔色
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: true,                   //是否显示分页（*）
        sortable: true,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
        {#queryParams: oTableInit.queryParams,//传递参数（*）#}
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）,数据为json数组时写client，json对象时（有total和rows时）这里要为server方式，写client列表无数据
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 5,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        {#search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大#}
        strictSearch: true,
        showColumns: true,                  //是否显示所有的列
        showRefresh: true,                  //是否显示刷新按钮
        minimumCountColumns: 2,             //最少允许的列数
        clickToSelect: true,                //是否启用点击选中行
        {#height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度#}
        uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
        showToggle: false,                    //是否显示详细视图和列表视图的切换按钮
        cardView: false,                    //是否显示详细视图
        detailView: false,                   //是否显示父子表
        idField: 'project_name',          //指定主键
        singleSelect: true,                //开启单选,想要获取被选中的行数据必须要有该参数

        //得到查询的参数，会在url后面拼接，如：?rows=5&page=2&sortOrder=asc&search_kw=&_=1564105760651
        queryParams: function (params) {
            //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            var query_params = {
                rows: params.limit,                         //页面大小
                page: (params.offset / params.limit) + 1,   //页码
                sort: params.sort,      //排序列名
                sortOrder: params.order, //排位命令（desc，asc）

                //查询框中的参数传递给后台
                search_kw: $('#search-keyword').val(), // 请求时向服务端传递的参数
            };
            return query_params;
        },

		columns: [
		
			{
                field: 'sid',
                title: '序号',
                width: 120,
            },
			
            {
                field: 'id',  　　　　　　//返回数据rows数组中的每个字典的键名与此处的field值要保持一致
                title: '商品图片 款式编码',
                width: 120,
            },
            {
                field: 'name',
                title: '库存量 版状态',
                width: 200,
            },
            {
                field: 'is_delete',
                title: '商品信息'
            },
            {
                field: 'operate',
                title: '操作',
                width: 120,
                align: 'center',
                valign: 'middle',
                formatter: actionFormatter,
             },

        ],
        onLoadSuccess: function(data){
             {#获取行数据的状态#}
            console.log(data);
            {#获取所有列表数据#}

            var data=$("#mytab").bootstrapTable("getData");
         
            {#根据每行数据的status值渲染开关#}

        }

    });


//操作栏的格式化,value代表当前单元格中的值，row代表当前行数据，index表示当前行的下标
function actionFormatter(value, row, index) {
    var id = index;
    var data = JSON.stringify(row);
    var result = "";
    result += "<a href='javascript:;' class='btn btn-xs green' onclick=\"EditViewById('" + id + "', view='view')\" title='查看'><span class='glyphicon glyphicon-search'></span></a>";
    {#result += "<a href='javascript:;' class='btn btn-xs blue' onclick=\"EditViewById('" + JSON.stringify(row) + "','" + id + "')\" title='编辑'><span class='glyphicon glyphicon-pencil'></span></a>";#}
    {#result += "<a href='javascript:;' class='btn btn-xs blue' onclick=\"EditViewById('" + row + "','" + id + "')\" title='编辑'><span class='glyphicon glyphicon-pencil'></span></a>";#}
    result += "<a href='javascript:;' class='btn btn-xs blue' onclick=\"uploading()\" title='上传'><span class='glyphicon glyphicon-circle-arrow-up'></span></a>";
    result += "<a href='javascript:;' class='btn btn-xs red' onclick=\"use('" + id + "')\" title='删除'><span class='glyphicon glyphicon-remove'></span></a>";
    return result;

}
function EditViewById(id){

	alert(id)	
	alert("查看")
	                	
}

function use(id){
	alert(id)
	alert("使用")
}
function uploading(id){
	alert(id)
	alert("上传")
	
 }

// 搜索查询按钮触发事件
$(function() {
    $("#search-button").click(function () {
        $('#mytab').bootstrapTable(('refresh')); // 很重要的一步，刷新url！
        $('#search-keyword').val()
    })
})

//重置搜索条件
function clean(){
    //先清空
    $('#search-keyword').val('');
    //清空后查询条件为空了，再次刷新页面，就是全部数据了
    $('#mytab').bootstrapTable(('refresh')); // 很重要的一步，刷新url！
}

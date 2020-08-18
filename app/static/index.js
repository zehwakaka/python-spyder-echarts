// 立即执行函数，防止变量污染 (function() {})();

// 柱状图模块1
(function () {
  // 1.实例化对象
  var myChart = echarts.init(document.querySelector(".bar .chart"));
  // 2.指定配置项和数据
  var option = {
    legend:{
      data: []
    },
    color: ['#2f89cf'],
    // 提示框组件
    tooltip: {
      trigger: 'axis',
      axisPointer: { // 坐标轴指示器，坐标轴触发有效
        type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
      }
    },
    // 修改图表位置大小
    grid: {
      left: '0%',
      top: '10px',
      right: '0%',
      bottom: '4%',
      containLabel: true
    },
    // x轴相关配置
    xAxis: {
        type: 'category',
        data: [],
        show: true,
      axisTick: {
        alignWithLabel: true
      },
      // 修改刻度标签，相关样式
      axisLabel: {
        color: "rgba(255, 255, 255, 1)",
        fontSize: 10,
        show: true,
        interval:0 
      },
      // x轴样式不显示
      axisLine: {
        show: true
      },
      nameTextStyle: {
      color: "rgba(255, 255, 255, 1)"
    }
    },
    // y轴相关配置
    yAxis: [{
      type: 'value',
      // 修改刻度标签，相关样式
      axisLabel: {
        color: "rgba(255,255,255,0.6)",
        fontSize: 12
      },
      // y轴样式修改
      axisLine: {
        lineStyle: {
          color: "rgba(255,255,255,0.6)",
          width: 2
        }
      },
      // y轴分割线的颜色
      splitLine: {
        lineStyle: {
          color: "rgba(255,255,255,0.1)"
        }
      }
    }],
    // 系列列表配置
    series: [{
      name: '累计确诊',
      type: 'bar',
      barWidth: '35%',
      // ajax传动态数据
      data: [],
      itemStyle: {
        // 修改柱子圆角
        barBorderRadius: 1
      }
    }]
    
  };

  $.ajax({
    cache: false,
    type:"GET",
    url:"/province_top15_curconfirm",
    data: null,
    dataType : "json",
    async: false,
    error: function(request) {
        alert("发送请求失败！");
    },
    success: function(result) {
        // pub_date, privinces, curConfirms
        var myCars=new Array();
        for(i=0; i<result.privincestop15.length; ++i) {
            option.legend.data.push(result.privincestop15[i])
            option.xAxis.data.push(result.privincestop15[i])
            option.series[0].data.push({name:result.privincestop15[i], value:result.curConfirmstop15[i]})
        }

        console.info(result)
    }
});

  // 3.把配置项给实例对象
  myChart.setOption(option);

  // 4.让图表随屏幕自适应
  window.addEventListener('resize', function () {
    myChart.resize();
  })
})();

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 折线图模块1
(function () {
  

  var myChart = echarts.init(document.querySelector(".line .chart"));

  var option = {
    // 修改两条线的颜色
    color: ['#00f2f1', '#ed3f35'],
    tooltip: {
      trigger: 'axis'
    },
    // 图例组件
    legend: {
      data: [],
      // 当serise 有name值时， legend 不需要写data
      // 修改图例组件文字颜色
      textStyle: {
        color: '#4c9bfd'
      },
      right: '10%',
    },
    grid: {
      top: "20%",
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
      show: true, // 显示边框
      borderColor: '#012f4a' // 边框颜色
    },
    xAxis: {
      data: [],
      type: 'category',
      boundaryGap: false, // 去除轴间距
      // 去除刻度线
      axisTick: {
        show: false
      },
      axisLabel: {
        color: "#4c9bfb" // x轴文本颜色
      },
      axisLine: {
        show: false // 去除轴线
      }
    },
    yAxis: {
      type: 'value',
      // 去除刻度线
      axisTick: {
        show: false
      },
      axisLabel: {
        color: "#4c9bfb" // x轴文本颜色
      },
      axisLine: {
        show: false // 去除轴线
      },
      splitLine: {
        lineStyle: {
          color: "#012f4a"
        }
      }
    },
    series: [
      {
        type: 'line',
        smooth: true, // 圆滑的线
        name: '现存确诊',
        data: [],
      }
    ]
  };


   $.ajax({
    cache: false,
    type:"GET",
    url:"/home_daily_datas",
    data: null,
    dataType : "json",
    async: false,
    error: function(request) {
        alert("发送请求失败！");
    },
    success: function(result) {
        for(i=0; i<result.time.length; ++i){
          option.legend.data.push(result.time[i])
          option.xAxis.data.push(result.time[i])
          option.series[0].data.push({name:result.time[i], value:result.curConfirm[i]})
        }
        console.info(result)
    }
}); 

  myChart.setOption(option);

  // 4.让图表随屏幕自适应
  window.addEventListener('resize', function () {
    myChart.resize();
  })


})();
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 饼形图1
(function () {
  var myChart = echarts.init(document.querySelector(".pie .chart"));
  var option = {
    title:"",
    color: ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6","#7D7D7D"],
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      // 垂直居中,默认水平居中
      // orient: 'vertical',
      data: [],
      bottom: 0,
      left: 10,
      // 小图标的宽度和高度
      itemWidth: 10,
      itemHeight: 10,
      // 修改图例组件的文字为 12px
      textStyle: {
        color: "rgba(255,255,255,.5)",
        fontSize: "10"
      }
    },
    series: [{
      name: '省份',
      type: 'pie',
      // 设置饼形图在容器中的位置
      center: ["50%", "42%"],
      // 修改饼形图大小，第一个为内圆半径，第二个为外圆半径
      radius: ['40%', '60%'],
      avoidLabelOverlap: false,
      // 图形上的文字
      label: {
        show: false,
        position: 'center'
      },
      // 链接文字和图形的线
      labelLine: {
        show: false
      },
      data: []
    }]
  };

  $.ajax({
    cache: false,
    type:"GET",
    url:"/province_top5_curconfirm",
    data: null,
    dataType : "json",
    async: false,
    error: function(request) {
        alert("发送请求失败！");
    },
    success: function(result) {
        // pub_date, privinces, curConfirms
        option.title.subtext = "数据更新时间： "+result.pub_date
        for(i=0; i<result.privinces.length; ++i) {
            option.legend.data.push(result.privinces[i])
            option.series[0].data.push({name:result.privinces[i], value:result.curConfirms[i]})
        }
        console.info(result)
    }
});

  myChart.setOption(option);
  window.addEventListener('resize', function () {
    myChart.resize();
  })
})();











(function () {
  var myChart = echarts.init(document.querySelector(".map .chart"));
  
  var option = {
    backgroundColor: 'rgba(128, 128, 128, 0)',
    tooltip: {
        trigger: 'item',
        formatter: "省份：{b}<br/>确诊：{c}"
    },
    textStyle: {color: '#FFFFFF'},
    title:{
        left: 'center',
        text: '中国疫情地图（现有确诊人数）',
        subtext: '数据更新时间: ',
        textStyle:{
          color:"rgba(255, 255, 255)",
          fontSize:20,
          align:"center"
      }
    },
    visualMap: {
        left: 'left',
        top: 'bottom',
        splitNumber: 7,
        pieces: [
            {value: 0},
            {min: 0, max: 9},
            {min: 10, max: 49}, 
            {min: 50, max: 99},
            {min: 100, max: 999}, 
            {min: 1000, max: 9999}, 
            {min: 10000}
        ],
        textStyle: {
            color: "#fff"
        },
        inRange: {
            color: ["#FFFFFF", "#FFE5DB", "#FFC4B3", "#FF9985", "#F57567", "#E64546", "#B80909"]
        },
        outOfRange: {
            color: "#FFFFFF"
        },
        show:true
    },
    geo:{
        map:'china',
        roam:false,//不开启缩放和平移
        zoom:1.00,//视角缩放比例
        label: {
            normal: {
                show: true,
                fontSize:'11',
                color: '#6C6C6C'
            }
        },
        itemStyle: {
            normal:{
                borderColor: 'rgba(0, 0, 0, 0.2)'
            },
            emphasis:{
                areaColor: '#FFFF00',//鼠标悬停区域颜色
                shadowOffsetX: 0,
                shadowOffsetY: 0,
                shadowBlur: 20,
                borderWidth: 0,
                shadowColor: 'rgba(255, 255, 255, 0.5)'
            }
        }
    },
    series:[{
        name:'现有确诊',
        type:'map',
        map:'china',
        geoIndex: 0,
        roam: true,
        label: {
            normal: {
                show: true,
                textStyle:{
                    color: 'rgb(0, 0, 0)',
                    fontSize: 14
                }
            }
        },
        data:[]
    }]
};

$.ajax({
    cache: false,
    url:'/get_province_currentConfirmedCount',
    type:"GET",
    dataType:'json',
    async:false,
    error: function(request) {
        alert("发送请求失败！");
    },
    success: function(result) {
        console.info(result)
        for(i=0,max=result.provinceShortName.length; i<max; ++i) {
            option.series[0].data.push({name:result.provinceShortName[i], value:result.currentConfirmedCount[i]})
        }
        option.title.subtext = '数据更新时间: ' + result.pub_date
    }
});





  myChart.setOption(option);
  window.addEventListener('resize', function () {
    myChart.resize();
  })
})();


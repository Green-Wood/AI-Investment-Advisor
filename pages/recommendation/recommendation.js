// pages/recommendation/recommendation.js
import * as echarts from '../../ec-canvas/echarts';

const app = getApp();

function initRadarChart(canvas, width, height) {
  const chart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(chart);
  var option = {
    backgroundColor: "#ffffff",
    color: ["#37A2DA", "#FF9F7F"],
    tooltip: {},
    xAxis: {
      show: false
    },
    yAxis: {
      show: false
    },
    radar: {
      // shape: 'circle',
      indicator: [{
        name: '股票型',
        max: 500
      },
      {
        name: '联接型',
        max: 500
      },
      {
        name: 'QDII',
        max: 500
      },
      {
        name: '混合型',
        max: 500
      },
      {
        name: '货币型',
        max: 500
      },
      {
        name: '债券型',
        max: 500
      }
      ]
    },
    series: [{
      name: '预算 vs 开销',
      type: 'radar',
      data: [{
        value: [430, 340, 500, 300, 490, 400],
        name: '预算'
      },
      {
        value: [300, 430, 150, 300, 420, 250],
        name: '开销'
      }
      ]
    }]
  };
  chart.setOption(option);
  return chart;
}

function initLineChart(canvas, width, height) {
  const chart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(chart);
  var option = {
    title: {
      text: '基金走势',
      left: 'center'
    },
    color: ["#37A2DA", "#9370DB"],
    legend: {
      data: ['A', 'C'],
      top: 25,
      left: 'center',
      backgroundColor: 'cyan',
      z: 100
    },
    grid: {
      containLabel: true
    },
    tooltip: {
      show: true,
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      // show: false
    },
    yAxis: {
      x: 'center',
      type: 'value',
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
      // show: false
    },
    series: [{
      name: 'A',
      type: 'line',
      smooth: true,
      data: [18, 36, 65, 30, 78, 40, 33]
    },{
      name: 'C',
      type: 'line',
      smooth: true,
      data: [10, 30, 31, 50, 40, 20, 10]
    }]
  };
  chart.setOption(option);
  return chart;
}

Page({
  onShareAppMessage: function (res) {
    return {
      title: 'ECharts 可以在微信小程序中使用啦！',
      path: '/pages/recommendation/recommendation',
      success: function () { },
      fail: function () { }
    }
  },
  data: {
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    },
    ecline: {
      onInit: initLineChart
    },
    ecradar: {
      onInit: initRadarChart
    }
  },
  onReady() {
  }
});

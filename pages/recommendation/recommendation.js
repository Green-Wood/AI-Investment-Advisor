// pages/recommendation/recommendation.js
import * as echarts from '../../ec-canvas/echarts';

var barec = null;

const app = getApp();

Page({
  data: {
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    },
    // ecradar: {
    //   onInit: initRadarChart
    // },
    ecline: {
      onInit: initLineChart
    },
    ec: { 
      onInit: function (canvas, width, height) { 
        barec = echarts.init(canvas, null, { 
          width: width, 
          height: height 
        }); 
        canvas.setChart(barec); 
        return barec;
      }
    },
  },
  onReady() {
    setTimeout(this.getData, 500);
  },
  onLoad: function (options) {
    this.setData({
      Risk_level: options.Risk_level
    })
    console.log(this.data.Risk_level)
    this.echartsComponent = this.selectComponent('#mychart')
    this.getData();
  },
  getData: function () {
    var that = this
    wx.request({
      url: 'https://49.234.212.86/api/info',
      data: {
        risk_value: this.data.Risk_level,
      },
      method: 'GET',
      header: { 'Content-Type': 'json' },

      success: (res) => {
        console.log(res.data.info.ratio)
        var data = res.data.info.ratio
        barec.setOption({
          backgroundColor: "#ffffff",
          color: ["#37A2DA", "#FF9F7F"],
          tooltip: {},
          radar: {
            indicator: [{ name: '股票型Stock', max: 0.0000001 },
            { name: '联接型Related', max: 0.01 },
            { name: 'QDII', max: 0.01 },
            { name: '混合型Hybrid', max: 0.00000018 },
            { name: '货币型Money', max: 0.01 },
            { name: '债券型Bond', max: 1 },
            { name: '其他Other', max: 0.005 }]
          },
          series: [{
            type: 'radar',
            data: [{
              value: [data.Stock, data.Related, data.QDII, data.Hybrid, data.Money, data.Bond, data.Other],
              }]
          }],
        })
        that.setData({
          rtrn: res.data.info.ans.Return.toFixed(5),
          volatility: res.data.info.ans.Volatility.toFixed(5),
          sharpRatio: res.data.info.ans.SharpRatio.toFixed(4),
        })
      },
    })
  },
})

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
    }, {
      name: 'C',
      type: 'line',
      smooth: true,
      data: [10, 30, 31, 50, 40, 20, 10]
    }]
  };
  chart.setOption(option);
  return chart;
}

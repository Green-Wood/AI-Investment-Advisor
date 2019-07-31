// pages/ask_risk/ask_risl.js

// 导航栏设置
const app = getApp()

Page({
  // skipToRiskChoices: function (options) {
  //   wx.navigateTo({
  //     url: '../index/index'
  //   })
  // },
  data: {
    // 组件所需的参数
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    },

    // 此页面 页面内容距最顶部的距离
    height: app.globalData.height * 2 + 20,
  },
  onLoad() {
    console.log(this.data.height)
  },
  skipToRiskChoices: function(){
    wx.navigateTo({
      url: '../index/index',
    })
  }
})
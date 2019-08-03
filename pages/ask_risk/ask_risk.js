// pages/ask_risk/ask_risl.js

// 导航栏设置
const app = getApp()

Page({
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
  jumpToRiskTest:function(){
    wx.navigateTo({
      url: '../risk_test/risk_test',
    })
  },

  onTap: function () {
    wx.showModal({
      title: '提示',
      content: '确定要跳过风险测评，直接去投资吗？',
      success: function (res) {
        if (res.confirm) {
          console.log('用户点击确定')
          {
            wx.navigateTo({
              url: '../index/index',
            })
          }
        } else if (res.cancel) {
          console.log('用户点击取消')
          {
            wx.navigateTo({
              url: '../ask_risk/ask_risk',
            })
          }
        }
      }
    })
  }
})

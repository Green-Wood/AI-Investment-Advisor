//index.js
//获取应用实例
const app = getApp();
// var str1 = "谨慎型"
// var str2 = "稳健型"
// var str3 = "平衡型"
// var str4 = "进取型"
// var str5 = "激进型"

Page({
  data: {
    str: 1,
// 组件所需的参数
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    }
  },
  changeSlider1(e) {
    this.setData({ str: e.detail.value })
    // if (e.detail.value == 1) {
    //   this.setData({ str: e.detail.value })
    // }
    // else if (e.detail.value == 2) {
    //   this.setData({ str: e.detail.value })
    // }
    // else if (e.detail.value == 3) {
    //   this.setData({ str: e.detail.value })
    // }
    // else if (e.detail.value == 4) {
    //   this.setData({ str: e.detail.value })
    // }
    // else if (e.detail.value == 5) {
    //   this.setData({ str: e.detail.value })
    // }
  },

  jumpToRecommendation: function (options) {
    wx.navigateTo({
      url: '../recommendation/recommendation'
    })
  },

  

})

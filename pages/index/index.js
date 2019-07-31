//index.js
//获取应用实例
const app = getApp();
var str1 = "谨慎型"
var str2 = "稳健型"
var str3 = "平衡型"
var str4 = "进取型"
var str5 = "激进型"

Page({
  data: {
    str: str1

  },
  changeSlider1(e) {
    if (e.detail.value == 1) {
      this.setData({ str: str1 })
    }
    else if (e.detail.value == 2) {
      this.setData({ str: str2 })
    }
    else if (e.detail.value == 3) {
      this.setData({ str: str3 })
    }
    else if (e.detail.value == 4) {
      this.setData({ str: str4 })
    }
    else if (e.detail.value == 5) {
      this.setData({ str: str5 })
    }
  },

  jumpToRecommendation: function (options) {
    wx.navigateTo({
      url: '../recommendation/recommendation'
    })
  },
})


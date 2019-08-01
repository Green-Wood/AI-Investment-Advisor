//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    slider1: 1,
  },
  changeSlider1(e) {
    this.setData({slider1: e.detail.value})
  }
})

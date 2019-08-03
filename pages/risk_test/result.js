// pages/result/result.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    A: 2,
    B: 3,
    C: 5,
    D: 8,
    Mark: 0,
    Kind: 'unknow',
    str: 1,
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    }
  },

  whichKind: function () {
    this.data.Mark = this.data.A * 2 + this.data.B * 3 + this.data.C * 5 + this.data.D * 8
    if (this.data.Mark >= 0 && this.data.Mark <= 18) {
      return "谨慎型-等级1"
    } else if (this.data.Mark > 18 && this.data.Mark <= 26) {
      return "稳健型-等级2"
    } else if (this.data.Mark > 26 && this.data.Mark <= 34) {
      return "平衡型-等级3"
    } else if (this.data.Mark > 34 && this.data.Mark <= 40) {
      return "进取型-等级4"
    } else if (this.data.Mark > 40){
      return "激进型-等级5"
    }

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

    this.setData({
      A: options.A - 0,
      B: options.B - 0,
      C: options.C - 0,
      D: options.D - 0,
    })

    this.setData({
      Mark: this.data.A * 2 + this.data.B * 3 + this.data.C * 5 + this.data.D * 8,
      Kind: this.whichKind()
    })
    
    console.log(this.data.Mark)
    console.log(this.whichKind())
  },
  jumpToInvestment: function(){
    wx.navigateTo({
      url: '../index/index',
    })
  },
  jumpToHome_page: function(){
    wx.navigateTo({
      url:'../home_page/home_page'
    })
  }
})


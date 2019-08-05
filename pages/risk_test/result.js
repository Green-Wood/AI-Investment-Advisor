// pages/result/result.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    Mark: 0,
    Kind: 'unknow',
    Risk_level: 1,
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    }
  },

  whichKind: function () {
    if (this.data.Mark >= 0 && this.data.Mark <= 18) {
      this.data.Risk_level = 1
      return "谨慎型-等级1"
    } else if (this.data.Mark > 18 && this.data.Mark <= 26) {
      this.data.Risk_level = 2
      return "稳健型-等级2"
    } else if (this.data.Mark > 26 && this.data.Mark <= 34) {
      this.data.Risk_level = 3
      return "平衡型-等级3"
    } else if (this.data.Mark > 34 && this.data.Mark <= 42) {
      this.data.Risk_level = 4
      return "进取型-等级4"
    } else if (this.data.Mark > 42) {
      this.data.Risk_level = 5
      return "激进型-等级5"
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

    this.setData({
      A: options.A,
      B: options.B,
      C: options.C,
      D: options.D,
    })

    this.setData({
      Mark: this.data.Mark = this.data.A * 2 + this.data.B * 4 + this.data.C * 6 + this.data.D * 8,
      Kind: this.whichKind()
    })
  },
  jumpToRecommendation: function(options){
    console.log("ok")
    wx.redirectTo({
      url: '/pages/recommendation/recommendation?&Risk_level=' + this.data.Risk_level,
    })
  },
})


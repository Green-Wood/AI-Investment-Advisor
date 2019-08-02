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
    Kind: 'unknow'
  },

  whichKind: function () {
    this.data.Mark = this.data.A * 2 + this.data.B * 3 + this.data.C * 5 + this.data.D * 8
    if (this.data.Mark >= 0 && this.data.Mark <= 20) {
      return "谨慎型"
    } else if (this.data.Mark > 20 && this.data.Mark <= 28) {
      return "稳健型"
    } else if (this.data.Mark > 28 && this.data.Mark <= 36) {
      return "平衡型"
    } else if (this.data.Mark > 36 && this.data.Mark <= 44) {
      return "进取型"
    } else if (this.data.Mark > 44){
      return "激进型"
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

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})
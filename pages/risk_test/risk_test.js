// pages/test/test.js
const app = getApp()

Page({
  /**
   * 页面的初始数据
   */

  data: {
    nvabarData: { //导航栏
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    },
    index: 0, //指针作用
    realIndex: 0, //换题真实数据

    A: 0,
    B: 0,
    C: 0,
    D: 0,

    optionA: "A",
    optionB: "B",
    optionC: "C",
    optionD: "D",

    questionDetail: app.globalData.question[0].question,
    answerA: app.globalData.question[0].option.A,
    answerB: app.globalData.question[0].option.B,
    answerC: app.globalData.question[0].option.C,
    answerD: app.globalData.question[0].option.D,

    list: [0, 1, 2, 3, 4, 5],
    listABCD: ['A', 'B', 'C', 'D']
  },

  changeQuestion: function (index) {
    if (this.data.listABCD[index] == 'A') {
      this.setData({
        A: this.data.A + 1
      })
    }
    else if (this.data.listABCD[index] == 'B') {
      this.setData({
        B: this.data.B + 1
      })
    }
    else if (this.data.listABCD[index] == 'C') {
      this.setData({
        C: this.data.C + 1
      })
    }
    else if (this.data.listABCD[index] == 'D') {
      this.setData({
        D: this.data.D + 1
      })
    }
    this.setData({
      index: this.data.index + 1
    })
    if (this.data.index < 6) {
      wx.showToast({
          duration: 500
      })
    }
    if (this.data.index < 6) {
      this.setData({
        realIndex: this.data.realIndex + 1,
        questionDetail: app.globalData.question[this.data.realIndex].question,

        answerA: app.globalData.question[this.data.realIndex].option[this.data.listABCD[0]],
        answerB: app.globalData.question[this.data.realIndex].option[this.data.listABCD[1]],
        answerC: app.globalData.question[this.data.realIndex].option[this.data.listABCD[2]],
        answerD: app.globalData.question[this.data.realIndex].option[this.data.listABCD[3]],
      })
    }
    if (this.data.index == 6) {
      wx.redirectTo({
        url: '/pages/risk_test/result?A=' + this.data.A + '&B=' + this.data.B + '&C=' + this.data.C + '&D=' + this.data.D,
      })
    }
  },

  answerClickA: function () {
    this.changeQuestion(0)
  },

  answerClickB: function () {
    this.changeQuestion(1)
  },

  answerClickC: function () {
    this.changeQuestion(2)
  },
  answerClickD: function () {
    this.changeQuestion(3)
  },
  

})

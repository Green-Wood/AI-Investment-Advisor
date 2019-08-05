// pages/test/test.js
const app = getApp()

Page({
    data: {
    nvabarData: { //导航栏
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    },
    index: 0,
    numA: 0,
    numB: 0,
    numC: 0,
    numD: 0,

    questionDetail: app.globalData.question[0].question,
    answerA: app.globalData.question[0].option.A,
    answerB: app.globalData.question[0].option.B,
    answerC: app.globalData.question[0].option.C,
    answerD: app.globalData.question[0].option.D,

    listABCD: ["A", "B", "C", "D"]
  },

  changeQuestion: function (index) {
    if (this.data.listABCD[index] == "A") {
      this.setData({ numA: this.data.numA += 1 })
    } else if (this.data.listABCD[index] == "B") {
      this.setData({ numB: this.data.numB += 1 })
    } else if (this.data.listABCD[index] == "C") {
      this.setData({ numC: this.data.numC += 1 })
    } else if (this.data.listABCD[index] == "D") {
      this.setData({ numD: this.data.numD += 1 })
    }
    if (this.data.index == 5) {
      wx.redirectTo({
        url: '/pages/risk_test/result?A=' + this.data.numA + '&B=' + this.data.numB + '&C=' + this.data.numC + '&D=' + this.data.numD,
      })
    }
    else if (this.data.index < 5){
      this.setData({
        index: this.data.index += 1,
        questionDetail: app.globalData.question[this.data.index].question,
        answerA: app.globalData.question[this.data.index].option[this.data.listABCD[0]],
        answerB: app.globalData.question[this.data.index].option[this.data.listABCD[1]],
        answerC: app.globalData.question[this.data.index].option[this.data.listABCD[2]],
        answerD: app.globalData.question[this.data.index].option[this.data.listABCD[3]],
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
  }
})

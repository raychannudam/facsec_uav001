import { defineStore } from "pinia"

export const useAppStore = defineStore("app", {
  state: () => {
    return {
      isDisplayRightToast: false,
      rightToastStatus: "info",
      rightToastMessage: "This is a default message.",
      isDisplayConfirmPopupModel: false,
      popupMessage: "This is a default message",
      popupCallBack: undefined,
      popupFeedback: undefined,
      isPageLoading: false,
      myProfile: undefined,
    }
  },
  actions: {
    displayRightToast(status, message, displayTimeout = 5000) {
      this.rightToastStatus = status
      this.rightToastMessage = message
      this.isDisplayRightToast = true
      setTimeout(() => {
        this.isDisplayRightToast = false
      }, displayTimeout)
    },

    displayPageLoading(value) {
      this.isPageLoading = value
    },

    displayConfirmPopupModel(popupMessage, popupCallBack = () => {}) {
      this.popupFeedback = undefined
      this.popupMessage = popupMessage
      this.popupCallBack = popupCallBack
    },

    setPopupFeedback(feedback) {
      this.popupFeedback = feedback
    },
  },
})

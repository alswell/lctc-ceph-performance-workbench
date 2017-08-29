/**
 * Created by chenkang1 on 2017/7/2.
 */
export default {
  state: {
    selectedItems: [],
    selectedRowKeys: [],
    refresh: 1,
  },

  effects: {},

  reducers: {
    showModal (state, { payload: { key: key } }) {
      return { ...state, [key]: true }
    },
    hideModal (state, { payload: { key: key } }) {
      return { ...state, [key]: false }
    },
    updateSelectItems (state, { payload: [selectedRowKeys, selectedItems] }) {
      return {
        ...state,
        selectedRowKeys,
        selectedItems,
      }
    },
    refresh (state) {
      return {
        ...state,
        refresh: ++state.refresh,
      }
    },
  },
}

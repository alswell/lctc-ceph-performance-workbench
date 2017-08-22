/**
 * Created by chenkang1 on 2017/6/30.
 */
import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'dva'
import DataTable from '../../components/BasicTable/DataTable'
import { Modal, Row, Col, Card, Button, Tabs } from 'antd'
import { Link } from 'dva/router'
import DropOption from '../../components/DropOption/DropOption'
import MemModal from '../../components/modals/MemModal'
import CpuModal from '../../components/modals/CpuModal'
import { fetchAndNotification } from '../../services/restfulService'

const confirm = Modal.confirm
const TabPane = Tabs.TabPane;

class SysInfo extends React.Component {
  // constructor (props) {
  //   super(props)
  // }

  componentDidMount () {

  }

  handleMenuClick = (record, e) => {
    if (e.key === '1') {
      let { dispatch } = this.props
      dispatch({
        type: 'sysinfo/showModal',
        payload: {
          key: 'modalVisible',
        },

      })
    } else if (e.key === '2') {
      confirm({
        title: 'Are you sure delete this record?',
        onOk () {
          console.log(record)
        },
      })
    }
  };

  showModal = (key) => {
    let { dispatch } = this.props
    dispatch({
      type: 'sysinfo/showModal',
      payload: {
        key,
      },
    })
  };

  refresh = () => {
    this.props.dispatch({ type: 'sysinfo/refresh' })
  };

  init = () => {
    this.modalProps = {
      visible: this.props.host.modalVisible,
      maskClosable: true,
      title: 'test',
      wrapClassName: 'vertical-center-modal',
      onOk: (data) => {
        console.log(data)
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'sysinfo/hideModal',
          payload: {
            key: 'modalVisible',
          },
        })
      },
    }

    this.hwinfotableDataProps = {
      columns: [
        {
          title: 'Job ID',
          dataIndex: 'jobid',
          key: 'jobid',
          width: 60,
          sorter: true,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          width: 80,
        }, {
          title: 'HyperThreading',
          dataIndex: 'HyperThreading',
          key: 'HyperThreading',
          // width: 100,
        }, {
          title: 'VirtualTechnology',
          dataIndex: 'VirtualTechnology',
          key: 'VirtualTechnology',
          // width: 64,
        }, {
          title: 'NUMA',
          dataIndex: 'NUMA',
          key: 'NUMA',
        },
        {
          title: 'OperatingModes',
          dataIndex: 'OperatingModes',
          key: 'OperatingModes',
        }, {
          title: 'CPUType',
          dataIndex: 'CPUType',
          key: 'CPUType',
        }, {
          title: 'CPUCores',
          dataIndex: 'CPUCores',
          key: 'CPUCores',
        },
        {  
          title: 'CPUMaxSpeed',
          dataIndex: 'CPUMaxSpeed',
          key: 'CPUMaxSpeed',
        }, {
          title: 'CPUNum',
          dataIndex: 'CPUNum',
          key: 'CPUNum',
        }, {
          title: 'MemNum',
          dataIndex: 'MemNum',
          key: 'MemNum',
        }, {
          title: 'MemType',
          dataIndex: 'MemType',
          key: 'MemType',
        }, {
          title: 'MemSize',
          dataIndex: 'MemSize',
          key: 'MemSize',
        }, 
      ],
      fetchData: {
        url: this.props.host.caseid ? `hwinfo/${this.props.host.caseid}/`:`hwinfo`,
        params: null,
      },
      errorMsg: 'get sar cpu table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'sysinfo/updateSelectItems', payload: selectedRows })
      },
    }

    this.osinfotableDataProps = {
      columns: [
        {
          title: 'Job ID',
          dataIndex: 'jobid',
          key: 'jobid',
          width: 60,
          sorter: true,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          width: 80,
        }, {
          title: 'PIDnumber',
          dataIndex: 'PIDnumber',
          key: 'PIDnumber',
        }, {
          title: 'read_ahead',
          dataIndex: 'read_ahead',
          key: 'read_ahead',
        }, {
          title: 'IOscheduler',
          dataIndex: 'IOscheduler',
          key: 'IOscheduler',
        },
        {
          title: 'dirty_background_ratio',
          dataIndex: 'dirty_background_ratio',
          key: 'dirty_background_ratio',
        }, {
          title: 'dirty_ratio',
          dataIndex: 'dirty_ratio',
          key: 'dirty_ratio',
        }, {
          title: 'MTU',
          dataIndex: 'MTU',
          key: 'MTU',
        },
      ],
      fetchData: {
        url: this.props.host.caseid ? `osinfo/${this.props.host.caseid}/`:`osinfo`,
        params: null,
      },
      errorMsg: 'get osinfo table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'sysinfo/updateSelectItems', payload: selectedRows })
      },
    }

    this.diskinfotableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          width: 80,
        }, {
          title: 'Name',
          dataIndex: 'disk_name',
          key: 'disk_name',
        }, {
          title: 'Size',
          dataIndex: 'disk_size',
          key: 'disk_size',
        }, {
          title: 'Model',
          dataIndex: 'disk_model',
          key: 'disk_model',
        }, {
          title: 'Speed',
          dataIndex: 'disk_speed',
          key: 'disk_speed',
        },
      ],
      fetchData: {
        url: this.props.host.caseid ? `diskinfo/${this.props.host.caseid}/`:`diskinfo`,
        params: null,
      },
      errorMsg: 'get diskinfo table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'sysinfo/updateSelectItems', payload: selectedRows })
      },
    }

    this.batchModalProps = {
      visible: this.props.host.batchModalVisible,
      maskClosable: true,
      title: '',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      fetchData: {
        url: 'host',
        method: 'delete',
      },
      onOk: (data) => {
        this.batchModalProps.onCancel()
        this.props.host.selectedItems.forEach((item) => {
          fetchAndNotification({
            url: 'host',
            method: 'delete',
            params: { ids: item.id },
            notifications: {
              title: 'batch Action',
              success: `${item.name} 操作成功！`,
              error: `${item.name} 操作失败！`,
            },
          })
        })
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'sysinfo/hideModal',
          payload: {
            key: 'batchModalVisible',
          },
        })
      },
    }

    this.createModalProps = {
      visible: this.props.host.createModalVisible,
      maskClosable: true,
      title: 'Batch Action Modal',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      fetchData: {
        url: 'host',
        method: 'delete',
      },
      onOk: (data) => {
        this.batchModalProps.onCancel()
        this.props.host.selectedItems.forEach((item) => {
          fetchAndNotification({
            url: 'host',
            method: 'delete',
            params: { ids: item.id },
            notifications: {
              title: 'batch Action',
              success: `${item.name} 操作成功！`,
              error: `${item.name} 操作失败！`,
            },
          })
        })
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'sysinfo/hideModal',
          payload: {
            key: 'createModalVisible',
          },
        })
      },
    }
  };

  state = {
    visible: false,
  };
  
  showModalchart = () => {
    this.setState({ visible: true })
  };

  handleCancel = () => {
    this.setState({ visible: false })
  };

  render () {
    this.init()

    return (
      <div className="content-inner">
        <Tabs type="card">
          <TabPane tab="hwinfo" key="1">
            <DataTable
              {...this.hwinfotableDataProps}
            />
          </TabPane>
          <TabPane tab="osinfo" key="2">
            <DataTable
              {...this.osinfotableDataProps}
            />
          </TabPane>
          <TabPane tab="diskinfo" key="3">
            <DataTable
              {...this.diskinfotableDataProps}
            />
          </TabPane>
        </Tabs>
      </div>
    )
  }
}


function mapStateToProps ({ sysinfo }) {
  return {
    host:sysinfo,
  }
}

SysInfo.propTypes = {
  cluster: PropTypes.object,
  location: PropTypes.object,
  dispatch: PropTypes.func,
  loading: PropTypes.object,
  host: PropTypes.object,
}

export default connect(mapStateToProps)(SysInfo)


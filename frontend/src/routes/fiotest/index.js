/**
 * Created by chenkang1 on 2017/6/30.
 */
import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'dva'
import DataTable from '../../components/BasicTable/DataTable'
import { Modal, Row, Col, Card, Button, Table } from 'antd'
import { Link } from 'dva/router'
import DropOption from '../../components/DropOption/DropOption'
import FioTestModal from '../../components/modals/FioTestModal'
import { fetchAndNotification } from '../../services/restfulService'

const confirm = Modal.confirm

class FioTest extends React.Component {
  // constructor (props) {
  //   super(props)
  // }

  componentDidMount () {

  }

  handleMenuClick = (record, e) => {
    if (e.key === '1') {
      let { dispatch } = this.props
      dispatch({
        type: 'fiotest/showModal',
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
      type: 'fiotest/showModal',
      payload: {
        key,
      },
    })
  };

  refresh = () => {
    this.props.dispatch({ type: 'fiotest/refresh' })
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
          type: 'fiotest/hideModal',
          payload: {
            key: 'modalVisible',
          },
        })
      },
    }

    this.tableDataProps = {
      columns: [
        {
          title: 'Case Name',
          dataIndex: 'case_name',
          key: 'case_name',
          //width: 350,
          sorter: true,
        }, {
          title: 'Status',
          dataIndex: 'status',
          key: 'status',
          sorter: true,
        }, {
          title: 'Job ID',
          dataIndex: 'jobid',
          key: 'jobid',
          sorter: true,
        },  
        // {
        //   title: 'Block Size',
        //   dataIndex: 'blocksize',
        //   key: 'blocksize',
        //   sorter: true,
        // }, {
        //   title: 'IO Depth',
        //   dataIndex: 'iodepth',
        //   key: 'iodepth',
        //   sorter: true,
        // }, {
        //   title: 'Number Job',
        //   dataIndex: 'numberjob',
        //   key: 'numberjob',
        //   sorter: true,
        // },
        // {
        //   title: 'Image Number',
        //   dataIndex: 'imagenum',
        //   key: 'imagenum',
        // }, {
        //   title: 'clientnum',
        //   dataIndex: 'clientnum',
        //   key: 'clientnum',
        // }, {
        //   title: 'readwrite',
        //   dataIndex: 'readwrite',
        //   key: 'readwrite',
        // },
        {  
          title: 'Read IOPS',
          dataIndex: 'r_iops',
          key: 'r_iops',
        },{
          title: 'Write IOPS',
          dataIndex: 'w_iops',
          key: 'w_iops',
        }, {
          title: 'IOPS',
          dataIndex: 'iops',
          key: 'iops',
        }, {
          title: 'Read BW',
          dataIndex: 'r_bw',
          key: 'r_bw',
        }, {
          title: 'Write BW',
          dataIndex: 'w_bw',
          key: 'w_bw',
        }, {
          title: 'BW',
          dataIndex: 'bw',
          key: 'bw',
        }, {
          title: 'lat',
          dataIndex: 'lat',
          key: 'lat',
        },
        {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
        },{
          title: 'Sys data',
          //dataIndex: 'sysdata',
          //key: 'sysdate',
          render: (text, record) => <Link to={`sysdata?caseid=${record.id}`}>sys data</Link>,
        },{
          title: 'Perf dump',
          //dataIndex: 'sysdata',
          //key: 'sysdate',
          render: (text, record) => <Link to={`perfdump/${record.id}`}>perf dump</Link>,
        },
        {
          title: 'Operation',
          key: 'operation',
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Update' }, { key: '2', name: 'Delete' }]}
            />)
          },
        },
      ],
      fetchData: {
        url: this.props.host.jobid ? `fiotest/${this.props.host.jobid}/`:`fiotest`,
        params: null,
      },
      errorMsg: 'get fiotest table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'fiotest/updateSelectItems', payload: selectedRows })
      },
    }

    this.batchModalProps = {
      visible: this.props.host.batchModalVisible,
      maskClosable: true,
      title: '',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      fetchData: {
        url: 'fiotest',
        //method: 'delete',
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
          type: 'fiotest/hideModal',
          payload: {
            key: 'batchModalVisible',
          },
        })
      },
    }
  };


  render () {
    this.init()

    return (
      <div className="content-inner">
        <Row gutter={32}>
          <Col lg={24} md={24}>
            <Card title="远程数据">
              <div className="action-btn-container">
                <Button type="primary" onClick={this.refresh} icon="reload" />
                <Button type="primary" onClick={this.showModal.bind(this, 'batchModalVisible')}
                  disabled={this.props.host.selectedItems.length === 0}
                >IOPS Chart</Button>
              </div>
              <DataTable
                {...this.tableDataProps}
                scroll={{ x: 1600 }}
              />
            </Card>
          </Col>
        </Row>
        {this.props.host.modalVisible && <Modal {...this.modalProps} />}
        {this.props.host.batchModalVisible && <FioTestModal {...this.batchModalProps} />}
      </div>
    )
  }
}


function mapStateToProps ({ fiotest }) {
  return {
    host:fiotest,
  }
}

FioTest.propTypes = {
  cluster: PropTypes.object,
  location: PropTypes.object,
  dispatch: PropTypes.func,
  loading: PropTypes.object,
  host: PropTypes.object,
}

export default connect(mapStateToProps)(FioTest)


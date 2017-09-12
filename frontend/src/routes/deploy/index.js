/**
 * Created by chenkang1 on 2017/6/30.
 */
import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'dva'
import DataTable from '../../components/BasicTable/DataTable'
import { Modal, Row, Col, Card, Button, Form } from 'antd'
import { Link } from 'dva/router'
import DropOption from '../../components/DropOption/DropOption'
import { fetchAndNotification } from '../../services/restfulService'
import { CollectionsPage } from '../../components/deploy/CreateModal'
import { InitImagePage } from '../../components/deploy/InitImage'
const FormItem = Form.Item
const confirm = Modal.confirm



class HostPage extends React.Component {
  // constructor (props) {
  //   super(props)
  // }
  componentDidMount () {

  }

  handleMenuClick = (record, e) => {
    if (e.key === '1') {
      confirm({
        title: 'Are you sure deploy this Cluster?',
        onOk :()=> {
          console.log(record)
          fetchAndNotification({
            url: 'deploy',
            method: 'post',
            params: record,
            notifications: {
              title: 'deploy Action',
              success: `${record.name} 操作成功！`,
              error: `${record.name} 操作失败！`,
            },
          }).then((result)=>{
          //when the fetch successfully ,refresh the table
          this.refresh()
        })
        },
      })
    } else if (e.key === '2') {
      confirm({
        title: 'Are you sure delete this Cluster?',
        onOk :()=> {
          console.log(record)
          fetchAndNotification({
            url: 'cluster',
            method: 'delete',
            params: { id: record.id },
            notifications: {
              title: 'Delete Action',
              success: `${record.name} 操作成功！`,
              error: `${record.name} 操作失败！`,
            },
          }).then((result)=>{
          //when the fetch successfully ,refresh the table
          this.refresh()
        })
        },
      })
    } else if (e.key === '3') {
      confirm({
        title: 'Are you sure to get the current ceph config as default config?',
        onOk :()=> {
          console.log(record)
          fetchAndNotification({
            url: 'defaultcephconfig',
            method: 'post',
            params: { id: record.id },
            notifications: {
              title: 'get ceph config Action',
              success: `${record.name} 操作成功！`,
              error: `${record.name} 操作失败！`,
            },
          })
        },
      })
    }
  };

  showModal = (key) => {
    let { dispatch } = this.props
    dispatch({
      type: 'deploy/showModal',
      payload: {
        key,
      },
    })
  };

  refresh = () => {
    this.props.dispatch({ type: 'deploy/refresh' })
  };

  init = () => {
    this.modalProps = {
      visible: this.props.host.modalVisible,
      maskClosable: true,
      title: 'test',
      wrapClassName: 'vertical-center-modal',
      onOk: (data) => {
        console.log(clusterinfo)
        console.log(data)
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'deploy/hideModal',
          payload: {
            key: 'modalVisible',
          },
        })
      },
    }

    this.tableDataProps = {
      columns: [
        {
          title: 'ID',
          dataIndex: 'id',
          key: 'id',
          width: 50,
          sorter: true,
        },
        {
          title: 'Cluster Name',
          dataIndex: 'name',
          key: 'name',
          // width: 64,
          sorter: true,
        }, {
          title: 'status',
          dataIndex: 'status',
          key: 'status',
          sorter: true,
          width: 600,
        }, 
        {
          title: 'objectstore',
          dataIndex: 'objectstore',
          key: 'objectstore',
          sorter: true,
          // width: 100,
        },
        {
          title: 'Detail',
          render: (text, record) => <Link to={`cluster/${record.id}`}>Detail</Link>,
        },
        {
          title: 'ceph config',
          render: (text, record) => <Link to={`defaultcephconfig/${record.id}`}>Ceph Config</Link>,
        },
        {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Deploy' }, { key: '2', name: 'Delete' }, { key: '3', name: 'Get ceph config' }]}
            />)
          },
        }
      ],
      fetchData: {
        url: `cluster`,
        params: null,
      },
      errorMsg: 'get cluster table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "deploy/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }
  };

  actionCollectionsProps = {
    refresh:this.refresh
  };

  render () {
    this.init()

    return (
      <div className="content-inner">
        <Row gutter={32}>
          <Col lg={24} md={24}>
            <Card>
              <div className="action-btn-container">
                <CollectionsPage {...this.actionCollectionsProps}/>
                <Button type="primary" onClick={this.refresh} icon="reload" />
              </div>
              <DataTable
                {...this.tableDataProps}
              />
            </Card>
          </Col>
        </Row>
        {this.props.host.modalVisible && <InitImagePage {...this.modalProps}/>}
      </div>
    )
  }
}


function mapStateToProps ({ deploy }) {
  return {
    host:deploy,
  }
}

HostPage.propTypes = {
  cluster: PropTypes.object,
  location: PropTypes.object,
  dispatch: PropTypes.func,
  loading: PropTypes.object,
  host: PropTypes.object,
}

export default connect(mapStateToProps)(HostPage)


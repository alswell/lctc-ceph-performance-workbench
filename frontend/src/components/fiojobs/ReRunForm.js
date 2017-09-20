/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Form, Icon, Input, Button, Modal, Row, Col, Select, Checkbox } from 'antd'
const { TextArea } = Input;
import { Link } from 'dva/router'
import PropTypes from 'prop-types'
import './TestForm.less'
import { fetchAndNotification } from '../../services/restfulService'
const FormItem = Form.Item

function hasErrors (fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field])
}

class TestTestForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      spinning: true,
      data: {},
      clusters: {},
      clients: [],
      pools: [],
      imagecount: 0,
      images: [],
      setvaluejobname: false,
      setvaluebs: false,
      setvaluepoolname: false,
      setvalueiodepth: false,
      setvaluenumjob: false,
      setvaluerwmixread: false,
      setvaluecluster: false,
      setvalueimagename: false,
      setvalueimagecount: false,
      setvaluefiotype: false,
      setvalueruntime: false,
      setvaluefiopara: false,
      setvaluecephconfig: false,
      setvaluesysdata: false,
      setvalueclient: false,
    }
  }

  componentDidMount () {
    // To disabled submit button at the beginning.
    this.props.form.validateFields()
    if ( this.props.record.id != 0 ){this.fetchDetail()}
    this.fetchCluster()
  }

  fetchDetail = () => {
    fetchAndNotification({
      //url: `sarcpu?caseid=${this.state.id}`,
      url: `jobdetail?jobid=${this.props.record.id}`,
      method: 'get',
      notifications:{
        error: `获取数据失败！`,
      }
    }).then((result) => {
      this.setState({
        spinning: false,
        data: result.data
      })
    })
  }

  fetchCluster = () => {
    fetchAndNotification({
      url: `cluster`,
      method: 'get',
      notifications:{
        error: `获取数据失败！`,
      }
    }).then((result) => {
      this.setState({
        spinning: false,
        clusters: result.data.data
      })
    })
  }

  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values)

        this.props.onCancel()
        fetchAndNotification({
          url: 'create',
          method: 'post',
          params: values,
          notifications: {
            title: 'create Action',
            success: `创建${values.jobname} 操作成功！`,
            error: `创建${values.jobname} 操作失败！`,
          },
        }).then((result)=>{
          //when the fetch successfully ,refresh the table
          this.props.refresh()
        })
      }
    })
  };

  handleImagecountChange = (value) => {
    this.props.form.resetFields(['imagename']);
    const clustervalue = this.props.form.getFieldValue('cluster');
    for (let i=0; i<this.state.clusters.length; i++) {
      if (this.state.clusters[i].clustername == clustervalue ) {
        fetchAndNotification({
            url: `images/${this.state.clusters[i].id}/`,
            method: 'get',
            params: { imagecount: value },
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              images: result.data
            })
          })
      }
    }
  }

  handleChange = (value) => {
    //console.log(`selected ${value}`);
    for (let i=0; i<this.state.clusters.length; i++) {
      if (this.state.clusters[i].clustername == value) {
        fetchAndNotification({
          url: `clients?id=${this.state.clusters[i].id}`,
          method: 'get',
          notifications:{
            error: `获取数据失败！`,
          }
        }).then((result) => {
          this.setState({
            clients: result.data
           })
        })
        fetchAndNotification({
          url: `pools/${this.state.clusters[i].id}/`,
          method: 'get',
          notifications:{
            error: `获取数据失败！`,
          }
        }).then((result) => {
          this.setState({
            pools: result.data
          })
        })
        const imagecountvalue = this.props.form.getFieldValue('imagecount');
        fetchAndNotification({
            url: `images/${this.state.clusters[i].id}/`,
            method: 'get',
            params: { imagecount: imagecountvalue },
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              images: result.data
            })
          })
      }
    }
    this.props.form.resetFields(['imagename', 'poolname', 'client']);
  };


  render () {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched, getFieldValue, setFieldsValue } = this.props.form
    
    // Only show error after a field is touched.
    const userNameError = isFieldTouched('userName') && getFieldError('userName')
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 6 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 14 },
      },
    };
    const formItemLayoutWithOutLabel = {
      wrapperCol: {
        xs: { span: 24, offset: 0 },
        sm: { span: 11, offset: 6 },
      },
    };

    let gotoinitimage = []
    const clustervalue = getFieldValue('cluster')
    for (let i=0; i<this.state.clusters.length; i++) {
      if  (this.state.clusters[i].clustername == clustervalue) {
        gotoinitimage.push(<Link to={`cluster/${this.state.clusters[i].id}`}>Create image</Link>)
      }
    }
    const getcluster = [];
    if ( this.state.clusters.length > 0 ) {
      for (let i=0; i<this.state.clusters.length; i++) {
        getcluster.push(<Option key={this.state.clusters[i].clustername}>{this.state.clusters[i].clustername}</Option>)
      }
    }
    else{
      getcluster.push(<Option key={1}></Option>)
    }

    const rwmixread = [];
    for (let i = 0; i <= 100; i=i+10) {
      rwmixread.push(<Option key={i}>{i}</Option>);
    }

    let getclients = [];
    if ( this.state.clients.length > 0 ) {
      for (let i=0; i<this.state.clients.length; i++) {
        getclients.push(<Option key={this.state.clients[i]}>{this.state.clients[i]}</Option>)
      }
    }
    else{
      getclients.push(<Option key={1}></Option>)
    }
    
    let getpools = [];
    if ( this.state.pools.length > 0 ) {
      for (let i=0; i<this.state.pools.length; i++) {
        getpools.push(<Option key={this.state.pools[i]}>{this.state.pools[i]}</Option>)
      }
    }
    else{
      getpools.push(<Option key={1}></Option>)
    }

    let getimages = [];
    if ( this.state.images.length > 0 ) {
      for (let i=0; i<this.state.images.length; i++) {
        getimages.push(<Option key={this.state.images[i]}>{this.state.images[i]}</Option>)
      }
    }
    else{
      getimages.push(<Option key={1}></Option>)
    }

    let jobnamevalue = getFieldValue('jobname');
    if (this.props.visible && this.state.data.jobname != undefined && this.state.setvaluejobname == false && jobnamevalue != this.state.data.jobname ){
      setFieldsValue({
        jobname: this.state.data.jobname,
      });
      this.setState({
        setvaluejobname: true,
      })
    }
    if ( this.state.clients.length == 0 || this.state.pools.length == 0 ){
      for (let i=0; i<this.state.clusters.length; i++) {
        if (this.state.clusters[i].clustername == clustervalue ) {
          fetchAndNotification({
            url: `clients?id=${this.state.clusters[i].id}`,
            method: 'get',
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              clients: result.data
            })
          })
          fetchAndNotification({
            url: `pools/${this.state.clusters[i].id}/`,
            method: 'get',
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              pools: result.data
            })
          })
        }
      }
    }
    if ( this.props.visible && this.state.data.cluster != undefined && clustervalue != this.state.data.cluster && this.state.setvaluecluster == false ){
      setFieldsValue({
        cluster: this.state.data.cluster,
      });
      this.setState({
        setvaluecluster: true,
      })
    }
    const bsvalue = getFieldValue('bs');
    if ( this.props.visible && this.state.data.bs != undefined && bsvalue != this.state.data.bs && this.state.setvaluebs == false){
      setFieldsValue({
        bs: this.state.data.bs,
      });
      this.setState({
        setvaluebs: true,
      })
    }
    const fiotypevalue = getFieldValue('fiotype');
    if ( this.props.visible && this.state.data.fiotype != undefined && fiotypevalue != this.state.data.fiotype && this.state.setvaluefiotype == false ){
      setFieldsValue({
        fiotype: this.state.data.fiotype,
      });
      this.setState({
        setvaluefiotype: true,
      })
    }
    const rwmixreadvalue = getFieldValue('rwmixread');
    if ( this.props.visible && this.state.data.rwmixread != undefined && rwmixreadvalue != this.state.data.rwmixread && this.state.setvaluerwmixread == false ){
      setFieldsValue({
        rwmixread: this.state.data.rwmixread,
      });
      this.setState({
        setvaluerwmixread: true,
      })
    }
    const iodepthvalue = getFieldValue('iodepth');
    if ( this.props.visible && this.state.data.iodepth != undefined && iodepthvalue != this.state.data.iodepth && this.state.setvalueiodepth == false ){
      setFieldsValue({
        iodepth: this.state.data.iodepth,
      });
      this.setState({
        setvalueiodepth: true,
      })
    }
    const numjobvalue = getFieldValue('numjob');
    if ( this.props.visible && this.state.data.numjob != undefined && numjobvalue != this.state.data.numjob && this.state.setvaluenumjob == false ){
      setFieldsValue({
        numjob: this.state.data.numjob,
      });
      this.setState({
        setvaluenumjob: true,
      })
    }
    const imagenamevalue = getFieldValue('imagename');
    if ( this.props.visible && this.state.data.imagename != undefined && imagenamevalue != this.state.data.imagename && this.state.setvalueimagename == false ){
      setFieldsValue({
        imagename: this.state.data.imagename,
      });
      this.setState({
        setvalueimagename: true,
      })
    }
    const poolnamevalue = getFieldValue('poolname');
    if ( this.props.visible && this.state.data.poolname != undefined && poolnamevalue != this.state.data.poolname && this.state.setvaluepoolname == false ){
      setFieldsValue({
        poolname: this.state.data.poolname,
      });
      this.setState({
        setvaluepoolname: true,
      })
    }
    const runtimevalue = getFieldValue('runtime');
    if ( this.props.visible && this.state.data.runtime != undefined && runtimevalue != this.state.data.runtime && this.state.setvalueruntime == false ){
      setFieldsValue({
        runtime: this.state.data.runtime,
      });
      this.setState({
        setvalueruntime: true,
      })
    }
    const imagecountvalue = getFieldValue('imagecount');
    if ( this.props.visible && this.state.imagecount != imagecountvalue && imagecountvalue != undefined ) {
      this.setState({
          imagecount: imagecountvalue
      })
      for (let i=0; i<this.state.clusters.length; i++) {
        if (this.state.clusters[i].clustername == clustervalue ) {
          fetchAndNotification({
            url: `images/${this.state.clusters[i].id}/`,
            method: 'get',
            params: { imagecount: imagecountvalue },
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              images: result.data
            })
          })
        }
      }
    }
    if ( this.props.visible && this.state.data.imagecount != undefined && imagecountvalue != this.state.data.imagecount && this.state.setvalueimagecount == false ){
      setFieldsValue({
        imagecount: this.state.data.imagecount,
      });
      this.setState({
        setvalueimagecount: true,
      })
    }
    const fioparavalue = getFieldValue('fiopara');
    if ( this.props.visible && this.state.data.fiopara != undefined && fioparavalue != this.state.data.fiopara && this.state.setvaluefiopara == false ){
      setFieldsValue({
        fiopara: this.state.data.fiopara,
      });
      this.setState({
        setvaluefiopara: true,
      })
    }
    const cephconfigvalue = getFieldValue('cephconfig');
    if ( this.props.visible && this.state.data.cephconfig != undefined && cephconfigvalue != this.state.data.cephconfig && this.state.setvaluecephconfig == false ){
      setFieldsValue({
        cephconfig: this.state.data.cephconfig,
      });
      this.setState({
        setvaluecephconfig: true,
      })
    }
    const sysdatavalue = getFieldValue('sysdata');
    if ( this.props.visible && this.state.data.sysdata != undefined && sysdatavalue != this.state.data.sysdata && this.state.setvaluesysdata == false ){
      setFieldsValue({
        sysdata: this.state.data.sysdata,
      });
      this.setState({
        setvaluesysdata: true,
      })
    }
    const clientvalue = getFieldValue('client');
    if ( this.props.visible && this.state.data.clients != undefined && clientvalue != this.state.data.clients && this.state.setvalueclient == false ){
      //console.log(this.state.data.clients)
      setFieldsValue({
        client: this.state.data.clients,
      });
      this.setState({
        setvalueclient: true,
      })
    }
    console.log(getFieldsError())

    return (
      <Modal
        visible={this.props.visible}
        title="Create a new job"
        okText="Create"
        footer={null}
        onCancel={this.props.onCancel}
        width={800}
        // onOk={this.onCreate}
      >
        <Form onSubmit={this.handleSubmit}>
          <FormItem
            {...formItemLayout}
            label="JobName"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('jobname', {
              rules: [
                { required: true, message: 'Please input the jobname!' },
              ],
            })(
              <Input placeholder="Jobname" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Cluster"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('cluster', {
              rules: [
                { required: true, message: 'Please select read write type!' },
              ],
            })(
              <Select
                style={{ width: '100%' }}
                placeholder="Please select"
                onChange={this.handleChange}
              >
                {getcluster}
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Ceph Client"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('client', {
              rules: [{ required: true, message: 'Please select the client!' }],
            })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                 {getclients}
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="FioType & BlockSize"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('fiotype', {
              rules: [
                { required: true, message: 'Please select read write type!' },
              ],
            })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                <Option key="rw 4k">rw 4k</Option>
                <Option key="rw 8k">rw 8k</Option>
                <Option key="rw 16k">rw 16k</Option>
                <Option key="rw 32k">rw 32k</Option>
                <Option key="rw 64k">rw 64k</Option>
                <Option key="rw 128k">rw 128k</Option>
                <Option key="rw 256k">rw 256k</Option>
                <Option key="rw 512k">rw 512k</Option>
                <Option key="rw 1024k">rw 1024k</Option>
                <Option key="rw 2048k">rw 2048k</Option>
                <Option key="rw 4M">rw 4M</Option>
                <Option key="rw 8M">rw 8M</Option>
                <Option key="rw 16M">rw 16M</Option>
                <Option key="rw 32M">rw 32M</Option>
                <Option key="rw 64M">rw 64M</Option>
                <Option key="rw 128M">rw 128M</Option>
                <Option key="randrw 4k">randrw 4k</Option>
                <Option key="randrw 8k">randrw 8k</Option>
                <Option key="randrw 16k">randrw 16k</Option>
                <Option key="randrw 32k">randrw 32k</Option>
                <Option key="randrw 64k">randrw 64k</Option>
                <Option key="randrw 128k">randrw 128k</Option>
                <Option key="randrw 256k">randrw 256k</Option>
                <Option key="randrw 512k">randrw 512k</Option>
                <Option key="randrw 1024k">randrw 1024k</Option>
                <Option key="randrw 2048k">randrw 2048k</Option>
                <Option key="randrw 4M">randrw 4M</Option>
                <Option key="randrw 8M">randrw 8M</Option>
                <Option key="randrw 16M">randrw 16M</Option>
                <Option key="randrw 32M">randrw 32M</Option>
                <Option key="randrw 64M">randrw 64M</Option>
                <Option key="randrw 128M">randrw 128M</Option>
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="RW MixRead(%)"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('rwmixread', {
              rules: [
                { required: true, message: 'Please select the RW MixRead!' },
              ],
              })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                {rwmixread}
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="IODepth"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('iodepth', {
              rules: [
                { required: true, message: 'Please select IODepth!' },
              ],
            })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                <Option key="1">1</Option>
                <Option key="4">4</Option>
                <Option key="8">8</Option>
                <Option key="16">16</Option>
                <Option key="32">32</Option>
                <Option key="64">64</Option>
                <Option key="128">128</Option>
                <Option key="256">256</Option>
                <Option key="512">512</Option>
                <Option key="1024">1024</Option>
              </Select>
            )}
          </FormItem>
           <FormItem
            {...formItemLayout}
            label="Num Job"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('numjob', {
              rules: [
                { required: true, message: 'Please select Num Job!' },
              ],
            })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                <Option key="1">1</Option>
                <Option key="4">4</Option>
                <Option key="8">8</Option>
                <Option key="16">16</Option>
                <Option key="32">32</Option>
                <Option key="64">64</Option>
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Runtime(s)"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('runtime', {
              initialValue: "120",
              rules: [
                { required: true, message: 'Please input the Run Time!' },
              ],
            })(
              <Input placeholder="120" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Pool"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('poolname', {
              initialValue: "rbd",
              rules: [
                { required: true, message: 'Please input the Pool Name!' },
              ],
            })(
              <Select
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                {getpools}
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Image Count"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('imagecount', {
              rules: [
                { required: true, message: 'Please input the Image Count!' },
              ],
            })(
              <Select
                style={{ width: '100%' }}
                placeholder="Please select"
                onChange={this.handleImagecountChange}
              >
                <Option key="1">1</Option>
                <Option key="2">2</Option>
                <Option key="3">3</Option>
                <Option key="4">4</Option>
                <Option key="5">5</Option>
                <Option key="6">6</Option>
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Image Name"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('imagename', {
              rules: [
                { required: true, message: 'Please input the Image Name!', whitespace: true },
              ],
            })(
              <Select
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                {getimages}
              </Select>
            )}
            {gotoinitimage}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Ceph config"
            help={userNameError || ''}
          >
            {getFieldDecorator(`cephconfig`, {
              validateTrigger: ['onChange', 'onBlur'],
              rules: [{
                required: false,
                whitespace: true,
                message: "Please input ceph config.",
              }],
              })(
              <TextArea placeholder="debug_paxos=35" style={{ width: '100%', marginRight: 8, height: 100 }} />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="fio parameter"
            help={userNameError || ''}
          >
            {getFieldDecorator(`fiopara`, {
              validateTrigger: ['onChange', 'onBlur'],
              rules: [{
                required: false,
                whitespace: true,
                message: "Please input fio parameter.",
              }],
              })(
              <TextArea placeholder="rw=rw" style={{ width: '100%', marginRight: 8, height: 100 }} />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="sysdata collect"
          >
            {getFieldDecorator(`sysdata`, {
              initialValue: ['perfdump'],
              rules: [{
                required: false,
              }],
              })(
              <Checkbox.Group>
                <Row>
                  <Col span={3}><Checkbox value="sar">sar</Checkbox></Col>
                  <Col span={4}><Checkbox value="iostat">iostat</Checkbox></Col>
                  <Col span={6}><Checkbox value="cephstatus">ceph status</Checkbox></Col>
                  <Col span={6}><Checkbox value="perfdump">perf dump</Checkbox></Col>
                  <Col span={8}><Checkbox value="lsblk">lsblk&smartctl</Checkbox></Col>
                </Row>
              </Checkbox.Group>
            )}
          </FormItem>
          <FormItem>
            <Button
              type="primary"
              htmlType="submit"
              disabled={hasErrors(getFieldsError()) || imagenamevalue == undefined || clientvalue == undefined}
            >
              Create
            </Button>
          </FormItem>
        </Form>
      </Modal>
    )
  }
}

TestTestForm.propTypes = {
  form: PropTypes.object,
  onCancel: PropTypes.function,
  visible: PropTypes.boolean,
  record: PropTypes.array,
  data: PropTypes.array,
}

const TestForm = Form.create()(TestTestForm)

export default TestForm

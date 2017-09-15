/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Form, Icon, Input, Button, Modal, Row, Col, Select } from 'antd'
const { TextArea } = Input;
import PropTypes from 'prop-types'
import './TestForm.less'
import { fetchAndNotification } from '../../services/restfulService'
const FormItem = Form.Item

function hasErrors (fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field])
}

let nodenameid = 0;
let nodeipid = 0;
let nodepwid = 0;
let osddiskid = 0;
let osdjid = 0;
let nodeid = 0;
let clientnameid = 0;
let clientipid = 0;
let clientpwid = 0;

class TestTestForm extends React.Component {

  componentDidMount () {
    // To disabled submit button at the beginning.
    this.props.form.validateFields()
  }

  noderemove = (k) => {
    const { form } = this.props;

    const nodenamekeys = form.getFieldValue('nodenamekeys');
    const nodeipkeys = form.getFieldValue('nodeipkeys');
    const nodepwkeys = form.getFieldValue('nodepwkeys');

    if (nodeipkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      nodenamekeys: nodenamekeys.filter(key => key !== k),
      nodeipkeys: nodeipkeys.filter(key => key !== k),
      nodepwkeys: nodepwkeys.filter(key => key !== k),
    });
  }

  nodeadd = () => {
    nodeipid++;
    nodepwid++;
    nodenameid++;
    const { form } = this.props;

    const nodenamekeys = form.getFieldValue('nodenamekeys');
    const nodeipkeys = form.getFieldValue('nodeipkeys');
    const nodepwkeys = form.getFieldValue('nodepwkeys');
    const nextnodenameKeys = nodenamekeys.concat(nodenameid);
    const nextnodeipKeys = nodeipkeys.concat(nodeipid);
    const nextnodepwKeys = nodepwkeys.concat(nodepwid);

    form.setFieldsValue({
      nodenamekeys: nextnodenameKeys,
      nodeipkeys: nextnodeipKeys,
      nodepwkeys: nextnodepwKeys,
    });
  }

  osdremove = (k) => {
    const { form } = this.props;

    const osddiskkeys = form.getFieldValue('osddiskkeys');
    const osdjkeys = form.getFieldValue('osdjkeys');
    const nodekeys = form.getFieldValue('nodekeys');

    if (osddiskkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      osddiskkeys: osddiskkeys.filter(key => key !== k),
      osdjkeys: osdjkeys.filter(key => key !== k),
      nodekeys: nodekeys.filter(key => key !== k),
    });
  }

  osdadd = () => {
    osddiskid++;
    osdjid++;
    nodeid++;
    const { form } = this.props;

    const osddiskkeys = form.getFieldValue('osddiskkeys');
    const osdjkeys = form.getFieldValue('osdjkeys');
    const nodekeys = form.getFieldValue('nodekeys');
    const nextosddiskKeys = osddiskkeys.concat(osddiskid);
    const nextosdjKeys = osdjkeys.concat(osdjid);
    const nextnodeKeys = osdjkeys.concat(nodeid);

    form.setFieldsValue({
      osddiskkeys: nextosddiskKeys,
      osdjkeys: nextosdjKeys,
      nodekeys: nextnodeKeys,
    });
  }

  clientremove = (k) => {
    const { form } = this.props;

     const clientnamekeys = form.getFieldValue('clientnamekeys');
    const clientipkeys = form.getFieldValue('clientipkeys');
    const clientpwkeys = form.getFieldValue('clientpwkeys');

    if (clientipkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      clientnamekeys: clientnamekeys.filter(key => key !== k),
      clientipkeys: clientipkeys.filter(key => key !== k),
      clientpwkeys: clientpwkeys.filter(key => key !== k),
    });
  }

  clientadd = () => {
    clientipid++;
    clientpwid++;
    clientnameid++;
    const { form } = this.props;

    const clientnamekeys = form.getFieldValue('clientnamekeys');
    const clientipkeys = form.getFieldValue('clientipkeys');
    const clientpwkeys = form.getFieldValue('clientpwkeys');
    const nextclientnameKeys = clientipkeys.concat(clientnameid);
    const nextclientipKeys = clientipkeys.concat(clientipid);
    const nextclientpwKeys = clientpwkeys.concat(clientpwid);

    form.setFieldsValue({
      clientnamekeys: nextclientnameKeys,
      clientipkeys: nextclientipKeys,
      clientpwkeys: nextclientpwKeys,
    });
  }

  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values)

        this.props.onCancel()
        fetchAndNotification({
          url: 'cluster',
          method: 'post',
          params: values,
          notifications: {
            title: 'deploy Action',
            success: `创建${values.clustername} 操作成功！`,
            error: `创建${values.clustername} 操作失败！`,
          },
        }).then((result)=>{
          //when the fetch successfully ,refresh the table
          this.props.refresh()
        })
      }
    })
  };

  handleChange = (value) => {
      console.log(`selected  checked ${value}`);
    };


  render () {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched, getFieldValue } = this.props.form

    // Only show error after a field is touched.
    const userNameError = isFieldTouched('userName') && getFieldError('userName')
    const passwordError = isFieldTouched('password') && getFieldError('password')
    const emailError = isFieldTouched('email') && getFieldError('email')
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

    getFieldDecorator('nodenamekeys', { initialValue: [] });
    getFieldDecorator('nodeipkeys', { initialValue: [] });
    getFieldDecorator('nodepwkeys', { initialValue: [] });
    const nodenamekeys = getFieldValue('nodenamekeys');
    const nodeipkeys = getFieldValue('nodeipkeys');
    const nodepwkeys = getFieldValue('nodepwkeys');
   
    const nodeformItems = nodeipkeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayout}
          required={false}
          label='Node'
          nodenamekey={k}
          nodeipkey={k}
          nodepwkey={k}
        >
          <Row gutter={8}>
            <Col span={5}>
              <p>Name:</p>
            </Col>          
            <Col span={14}>
              {getFieldDecorator(`nodename-${k}`, {
                rules: [{ required: true, message: 'Please input the node name!' }],
              })(
                <Input size="large" placeholder="ceph-1"/>
              )}
            </Col>
          </Row>
          <Row gutter={8}>
            <Col span={5}>
              <p>External IP:</p>
            </Col>          
            <Col span={14}>
              {getFieldDecorator(`nodeip-${k}`, {
                rules: [{ required: true, message: 'Please input the node ip!' }],
              })(
                <Input size="large" placeholder="10.240.217.101"/>
              )}
            </Col>
          </Row>
          <Row gutter={8}>
            <Col span={5}>
              <p>Root Password:</p>
            </Col>
            <Col span={14}>
              {getFieldDecorator(`nodepw-${k}`, {
                rules: [{ required: true, message: 'Please input the root password!' }],
              })(
                <Input prefix={<Icon type="lock" style={{ fontSize: 13 }} />} type="password" placeholder="Password"/>
              )}
            </Col>
            <Col span={2}>
              {nodeipkeys.length > 0 ? (
                <Icon
                  className="dynamic-delete-button"
                  type="minus-circle-o"
                  disabled={nodeipkeys.length === 0}
                  onClick={() => this.noderemove(k)}
                />
              ) : null}
          </Col>
          </Row>
        </FormItem>
      );
    });

    const nodeselectItems = nodeipkeys.map((k, index) => {
      const node = getFieldValue(`nodename-${k}`)
      if ( node != undefined ) {
        return (
          <Option key={node}>{node}</Option>
        );
      }
      else {
        return (
          <Option key={1}></Option>
        );
      }
    });

    getFieldDecorator('osddiskkeys', { initialValue: [] });
    getFieldDecorator('osdjkeys', { initialValue: [] });
    getFieldDecorator('nodekeys', { initialValue: [] });
    const osddiskkeys = getFieldValue('osddiskkeys');
    const osdjkeys = getFieldValue('osdjkeys');
    const nodekeys = getFieldValue('nodekeys');
    const osdformItems = osddiskkeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayout}
          required={false}
          label='osd'
          osddiskkeys={k}
          osdjkeys={k}
          nodekeys={k}
        >
        <Row gutter={12}>
            <Col span={2}>
              <p>node:</p>
            </Col>
            <Col span={6}>
              {getFieldDecorator(`node-${k}`, {
                rules: [{ required: true, message: 'Please input the host!' }],
              })(
                <Select
                  style={{ width: '100%' }}
                  onChange={this.handleChange}
                >
                  {nodeselectItems}
                </Select>
              )}
            </Col>
            <Col span={2}>
              <p>disk:</p>
            </Col>
            <Col span={4}>
              {getFieldDecorator(`osddisk-${k}`, {
                rules: [{ required: true, message: 'Please input the osd disk!' }],
              })(
                <Input size="large" placeholder="/dev/sdb"/>
              )}
            </Col>
            <Col span={2}>
              <p>journal:</p>
            </Col>
            <Col span={4}>
              {getFieldDecorator(`osdj-${k}`, {
                rules: [{ required: true, message: 'Please input the osd journal disk!' }],
              })(
                <Input size="large" placeholder="/dev/sdc"/>
              )}
            </Col>
          <Col span={2}>
          {osddiskkeys.length > 0 ? (
            <Icon
              className="dynamic-delete-button"
              type="minus-circle-o"
              disabled={osddiskkeys.length === 0}
              onClick={() => this.osdremove(k)}
            />
          ) : null}
          </Col>
        </Row>
         </FormItem>
      );
    });

    getFieldDecorator('clientnamekeys', { initialValue: [] });
    getFieldDecorator('clientipkeys', { initialValue: [] });
    getFieldDecorator('clientpwkeys', { initialValue: [] });
    const clientnamekeys = getFieldValue('clientnamekeys');
    const clientipkeys = getFieldValue('clientipkeys');
    const clientpwkeys = getFieldValue('clientpwkeys');
   
    const clientformItems = clientipkeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayout}
          required={false}
          label='Client'
          clientnamekey={k}
          clientipkey={k}
          clientpwkey={k}
        >
          <Row gutter={8}>
            <Col span={5}>
              <p>Name:</p>
            </Col>          
            <Col span={14}>
              {getFieldDecorator(`clientname-${k}`, {
                rules: [{ required: true, message: 'Please input the client name!' }],
              })(
                <Input size="large" placeholder="client-1"/>
              )}
            </Col>
          </Row>
          <Row gutter={8}>
            <Col span={5}>
              <p>External IP:</p>
            </Col>          
            <Col span={14}>
              {getFieldDecorator(`clientip-${k}`, {
                rules: [{ required: true, message: 'Please input the client ip!' }],
              })(
                <Input size="large" placeholder="10.240.217.131"/>
              )}
            </Col>
          </Row>
          <Row gutter={8}>
            <Col span={5}>
              <p>Root Password:</p>
            </Col>
            <Col span={14}>
              {getFieldDecorator(`clientpw-${k}`, {
                rules: [{ required: true, message: 'Please input the root password!' }],
              })(
                <Input prefix={<Icon type="lock" style={{ fontSize: 13 }} />} type="password" placeholder="Password"/>
              )}
            </Col>
            <Col span={2}>
              {clientipkeys.length > 0 ? (
                <Icon
                  className="dynamic-delete-button"
                  type="minus-circle-o"
                  disabled={clientipkeys.length === 0}
                  onClick={() => this.clientremove(k)}
                />
              ) : null}
          </Col>
          </Row>
        </FormItem>
      );
    });

    return (
      <Modal
        visible={this.props.visible}
        title="Create a new job"
        okText="Create"
        footer={null}
        onCancel={this.props.onCancel}
        width={1000}
      >
        <Form onSubmit={this.handleSubmit}>
          <FormItem
            {...formItemLayout}
            label="Cluster Name"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('clustername', {
              rules: [
                { required: true, message: 'Please input the clustername!' },
              ],
            })(
              <Input placeholder="cluster name" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Public Network"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('publicnetwork', {
              rules: [
                { required: true, message: 'Please input the public network!' },
              ],
            })(
              <Input placeholder="192.168.1.0/24" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Cluster Network"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('clusternetwork', {
              rules: [
                { required: true, message: 'Please input the Cluster network!' },
              ],
            })(
              <Input placeholder="192.168.2.0/24" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Type"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('objectstore', {
              rules: [
                { required: true, message: 'Please input the object store!' },
              ],
            })(
              <Select defaultValue="filestore" style={{ width: 120 }} onChange={this.handleChange}>
                <Option value="bluestore">bluestore</Option>
                <Option value="filestore">filestore</Option>
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Journal Size"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('journalsize', {
              rules: [
                { required: true, message: 'Please input the Journal Size!' },
              ],
            })(
              <Input placeholder="10240" />
            )}
          </FormItem>
          {nodeformItems}
          <FormItem
            {...formItemLayoutWithOutLabel}
          >
            <Button type="dashed" onClick={this.nodeadd} style={{ width: '100%' }}>
              <Icon type="plus" /> Add Node
            </Button>
          </FormItem>
          {osdformItems}
          <FormItem
            {...formItemLayoutWithOutLabel}
          >
            <Button type="dashed" onClick={this.osdadd} style={{ width: '100%' }}>
              <Icon type="plus" /> Add osd
            </Button>
          </FormItem>
          {clientformItems}
          <FormItem
            {...formItemLayoutWithOutLabel}
          >
            <Button type="dashed" onClick={this.clientadd} style={{ width: '100%' }}>
              <Icon type="plus" /> Add Client
            </Button>
          </FormItem>
          <FormItem
          {...formItemLayout}
          required={false}
          label='Monitor'
          validateStatus={userNameError ? 'error' : ''}
          help={userNameError || ''}
        >
          {getFieldDecorator(`mon`, {
             rules: [{ required: true, message: 'Please select the Monitor!' }],
          })(
            <Select
              mode="multiple"
              style={{ width: '100%' }}
              onChange={this.handleChange}
            >
              {nodeselectItems}
            </Select>
          )}
         </FormItem>
          <FormItem>
            <Button
              type="primary"
              htmlType="submit"
              disabled={hasErrors(getFieldsError())}
            >
              Add
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
}

const TestForm = Form.create()(TestTestForm)

export default TestForm

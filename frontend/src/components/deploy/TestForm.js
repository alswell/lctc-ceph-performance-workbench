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

let nodeipid = 1;
let nodepwid = 1;
let osddiskid = 1;
let osdjid = 1;
class TestTestForm extends React.Component {

  componentDidMount () {
    // To disabled submit button at the beginning.
    this.props.form.validateFields()
  }

  noderemove = (k) => {
    const { form } = this.props;

    const nodeipkeys = form.getFieldValue('nodeipkeys');
    const nodepwkeys = form.getFieldValue('nodepwkeys');

    if (nodeipkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      nodeipkeys: nodeipkeys.filter(key => key !== k),
      nodepwkeys: nodepwkeys.filter(key => key !== k),
    });
  }

  nodeadd = () => {
    nodeipid++;
    nodepwid++;
    const { form } = this.props;

    const nodeipkeys = form.getFieldValue('nodeipkeys');
    const nodepwkeys = form.getFieldValue('nodepwkeys');
    const nextnodeipKeys = nodeipkeys.concat(nodeipid);
    const nextnodepwKeys = nodepwkeys.concat(nodepwid);

    form.setFieldsValue({
      nodeipkeys: nextnodeipKeys,
      nodepwkeys: nextnodepwKeys,
    });
  }

  osdremove = (k) => {
    const { form } = this.props;

    const osddiskkeys = form.getFieldValue('osddiskkeys');
    const osdjkeys = form.getFieldValue('osdjkeys');

    if (osddiskkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      osddiskkeys: osddiskkeys.filter(key => key !== k),
      osdjkeys: osdjkeys.filter(key => key !== k),
    });
  }

  osdadd = () => {
    osddiskid++;
    osdjid++;
    const { form } = this.props;

    const osddiskkeys = form.getFieldValue('osddiskkeys');
    const osdjkeys = form.getFieldValue('osdjkeys');
    const nextosddiskKeys = osddiskkeys.concat(osddiskid);
    const nextosdjKeys = osdjkeys.concat(osdjid);

    form.setFieldsValue({
      osddiskkeys: nextosddiskKeys,
      osdjkeys: nextosdjKeys,
    });
  }

  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values)

        this.props.onCancel()
        fetchAndNotification({
          url: 'deploy',
          method: 'post',
          params: values,
          notifications: {
            title: 'deploy Action',
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

  handleChange = (value) => {
      console.log(`selected ${value}`);
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

    getFieldDecorator('osddiskkeys', { initialValue: [] });
    getFieldDecorator('osdjkeys', { initialValue: [] });
    const osddiskkeys = getFieldValue('osddiskkeys');
    const osdjkeys = getFieldValue('osdjkeys');
    const osdformItems = osddiskkeys.map((k, index) => {
      return (
        <Row gutter={8}>
            <Col span={3}>
              <p>osd{k-1}</p>
            </Col>
            <Col span={2}>
              <p>disk:</p>
            </Col>
            <Col span={6}>
              {getFieldDecorator('osddisk-${k}', {
                rules: [{ required: true, message: 'Please input the client!' }],
              })(
                <Input size="large" placeholder="/dev/sdb"/>
              )}
            </Col>
            <Col span={2}>
              <p>journal:</p>
            </Col>
            <Col span={6}>
              {getFieldDecorator('osdj-${k}', {
                rules: [{ required: true, message: 'Please input the client!' }],
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
      );
    });

    getFieldDecorator('nodeipkeys', { initialValue: [] });
    getFieldDecorator('nodepwkeys', { initialValue: [] });
    const nodeipkeys = getFieldValue('nodeipkeys');
    const nodepwkeys = getFieldValue('nodepwkeys');
    const nodeformItems = nodeipkeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayout}
          required={false}
          label={k}
          nodeipkey={k}
          nodepwkey={k}
        >
          <Row gutter={8}>
            <Col span={5}>
              <p>External IP:</p>
            </Col>          
            <Col span={14}>
              {getFieldDecorator('nodeip-${k}', {
                rules: [{ required: true, message: 'Please input the client!' }],
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
              {getFieldDecorator('nodepw-${k}', {
                rules: [{ required: true, message: 'Please input the client!' }],
              })(
                <Input size="large" placeholder="passw0rd"/>
              )}
            </Col>
          </Row>
          <Row gutter={8}>
            <Col span={8}>
              {nodeipkeys.length > 0 ? (
                <Button type="dashed" onClick={() => this.noderemove(k)} style={{ width: '100%' }} disabled={nodeipkeys.length === 0}>
                  <Icon
                    className="dynamic-delete-button"
                    type="minus-circle-o"
                  />Remove this Node
                </Button>    
              ) : null}
            </Col>
          </Row>
        </FormItem>
      );
    });

  console.log(nodeipkeys)
    const nodeselectItems = nodeipkeys.map((k, index) => {
      console.log(getFieldValue('nodeip-1'))
      const node = getFieldValue('nodeip-${k}')
      return (
        <Option key={node}>{node}</Option>
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
        // onOk={this.onCreate}
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
            label="Node1"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            <Row gutter={8}>
              <Col span={5}>
                <p>External IP:</p>
              </Col>          
              <Col span={14}>
                {getFieldDecorator('nodeip-1', {
                  rules: [{ required: true, message: 'Please input the client!' }],
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
                {getFieldDecorator('nodepw-1', {
                  rules: [{ required: true, message: 'Please input the client!' }],
                })(
                  <Input size="large" placeholder="passw0rd"/>
                )}
              </Col>
            </Row>
          </FormItem>
          {nodeformItems}
          <FormItem
            {...formItemLayoutWithOutLabel}
          >
            <Row gutter={8}>
              <Col span={12}>
                <Button type="dashed" onClick={this.nodeadd} style={{ width: '100%' }}>
                  <Icon type="plus" /> Add Node
                </Button>
              </Col>
            </Row>
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="OSD"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            <Row gutter={8}>
              <Col span={2}>
                <p>node:</p>
              </Col>
              <Col span={6}>
              {getFieldDecorator('bs', {
                rules: [
                  { required: true, message: 'Please select Block Size!' },
                ],
                })(
                  <Select
                    mode="multiple"
                    style={{ width: '100%' }}
                    placeholder="Please select"
                    onChange={this.handleChange}
                  >
                  {nodeselectItems}
                  </Select>
              )}
              </Col>
              <Col span={2}>
                <p>disk:</p>
              </Col>
              <Col span={6}>
                {getFieldDecorator('osddisk-1', {
                  rules: [{ required: true, message: 'Please input the client!' }],
                })(
                  <Input size="large" placeholder="/dev/sdb"/>
                )}
              </Col>
              <Col span={2}>
                <p>journal:</p>
              </Col>
              <Col span={6}>
                {getFieldDecorator('osdj-1', {
                  rules: [{ required: true, message: 'Please input the client!' }],
                })(
                  <Input size="large" placeholder="/dev/sdc"/>
                )}
              </Col>
            </Row>
            {osdformItems}
            <Row gutter={8}>
              <Col span={5}>
                <Button type="dashed" onClick={this.osdadd} style={{ width: '100%' }}>
                  <Icon type="plus" /> Add osd
                </Button>
              </Col>
            </Row>
          </FormItem>
          
          <FormItem>
            <Button
              type="primary"
              htmlType="submit"
              disabled={hasErrors(getFieldsError())}
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
}

const TestForm = Form.create()(TestTestForm)

export default TestForm

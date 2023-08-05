# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 11:03:56
@LastEditTime: 2022-06-14 17:53:00
@LastEditors: HuangJianYi
@Description: ip模块
"""

from seven_cloudapp_frame.models.ip_base_model import *
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.enum import *


class SaveIpInfoHandler(ClientBaseHandler):
    """
    :description: 保存IP信息
    """
    @filter_check_params("ip_name")
    def get_async(self):
        """
        :description: 保存IP信息
        :param app_id：应用标识
        :param act_id：活动标识
        :param ip_id: ip标识
        :param ip_name：ip名称
        :param ip_pic：ip图片
        :param show_pic：展示图片
        :param sort_index：排序
        :param is_release：是否发布
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        ip_id = int(self.get_param("ip_id", 0))
        act_id = self.get_act_id()
        ip_name = self.get_param("ip_name")
        ip_pic = self.get_param("ip_pic")
        show_pic = self.get_param("show_pic")
        sort_index = int(self.get_param("sort_index", 0))
        is_release = int(self.get_param("is_release", 1))
        ip_type = int(self.get_param("ip_type", 0))
        ip_summary = self.get_param("ip_summary")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        ip_base_model = IpBaseModel(context=self)
        invoke_result_data = ip_base_model.save_ip_info(app_id, act_id, ip_id, ip_name, ip_pic, show_pic, sort_index, is_release, ip_type, ip_summary)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if invoke_result_data.data["is_add"] == True:
            # 记录日志
            self.create_operation_log(OperationType.add.value, invoke_result_data.data["new"].__str__(), "SaveIpInfoHandler", None, self.json_dumps(invoke_result_data.data["new"]), self.get_open_id(), self.get_user_nick())
        else:
            self.create_operation_log(OperationType.update.value, invoke_result_data.data["new"].__str__(), "SaveIpInfoHandler", self.json_dumps(invoke_result_data.data["old"]), self.json_dumps(invoke_result_data.data["new"]), self.get_open_id(), self.get_user_nick())
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["new"].id)


class IpInfoListHandler(ClientBaseHandler):
    """
    :description: 获取ip列表
    """
    def get_async(self):
        """
        :description: 获取ip列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param is_del: 是否回收站1是0否
        :param is_release: 是否发布1是0否
        :param page_index：页索引
        :param page_size：页大小
        :return: list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        is_del = int(self.get_param("is_del", 0))
        is_release = int(self.get_param("is_release", -1))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"
        condition = invoke_result_data.data["condition"] if invoke_result_data.data.__contains__("condition") else ""
        params = invoke_result_data.data["params"] if invoke_result_data.data.__contains__("params") else []
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc"
        page_list, total = IpBaseModel(context=self).get_ip_info_list(app_id, act_id, page_size, page_index, is_del, is_release, field, condition, params, order_by, is_cache=False)
        ref_params = {}
        page_info = PageInfo(page_index, page_size, total, self.business_process_executed(page_list, ref_params))
        return self.response_json_success(page_info)


class DeleteIpInfoHandler(ClientBaseHandler):
    """
    :description: 删除ip
    """
    @filter_check_params("ip_id")
    def get_async(self):
        """
        :description: 删除ip
        :param app_id：应用标识
        :param ip_id: ip标识
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        ip_id = int(self.get_param("ip_id", 0))

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ip_base_model = IpBaseModel(context=self)
        invoke_result_data = ip_base_model.update_ip_info_status(app_id, ip_id,1)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        self.create_operation_log(OperationType.delete.value, "ip_info_tb", "DeleteIpInfoHandler", None, ip_id)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class ReleaseIpInfoHandler(ClientBaseHandler):
    """
    :description: 上下架ip
    """
    @filter_check_params("ip_id")
    def get_async(self):
        """
        :description: 上下架ip
        :param app_id：应用标识
        :param ip_id: ip标识
        :param is_release: 是否发布 1-是 0-否
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        ip_id = int(self.get_param("ip_id", 0))
        is_release = int(self.get_param("is_release", 0))

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ip_base_model = IpBaseModel(context=self)
        invoke_result_data = ip_base_model.release_ip_info(app_id, ip_id, is_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class SaveIpTypeHandler(ClientBaseHandler):
    """
    :description: 保存IP类型
    """
    @filter_check_params("type_name")
    def get_async(self):
        """
        :description: 保存IP类型
        :param app_id：应用标识
        :param act_id：活动标识
        :param ip_type_id: ip类型标识
        :param type_name：类型名称
        :param sort_index：排序
        :param is_release：是否发布
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        ip_type_id = self.get_param_int("ip_type_id", 0)
        type_name = self.get_param("type_name")
        sort_index = self.get_param_int("sort_index", 0)
        is_release = self.get_param_int("is_release", 1)

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        ip_base_model = IpBaseModel(context=self)
        invoke_result_data = ip_base_model.save_ip_type(app_id, act_id, ip_type_id, type_name, sort_index, is_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if invoke_result_data.data["is_add"] == True:
            # 记录日志
            self.create_operation_log(OperationType.add.value, invoke_result_data.data["new"].__str__(), "SaveIpTypeHandler", None, self.json_dumps(invoke_result_data.data["new"]), self.get_open_id(), self.get_user_nick())
        else:
            self.create_operation_log(OperationType.update.value, invoke_result_data.data["new"].__str__(), "SaveIpTypeHandler", self.json_dumps(invoke_result_data.data["old"]), self.json_dumps(invoke_result_data.data["new"]), self.get_open_id(), self.get_user_nick())
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["new"].id)


class IpTypeListHandler(ClientBaseHandler):
    """
    :description: 获取ip类型列表
    """
    def get_async(self):
        """
        :description: 获取ip列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param is_release: 是否发布1是0否
        :param page_index：页索引
        :param page_size：页大小
        :return: list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        is_release = self.get_param_int("is_release", -1)
        page_index = self.get_param_int("page_index", 0)
        page_size = self.get_param_int("page_size", 20)

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"
        condition = invoke_result_data.data["condition"] if invoke_result_data.data.__contains__("condition") else ""
        params = invoke_result_data.data["params"] if invoke_result_data.data.__contains__("params") else []
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc"
        page_list, total = IpBaseModel(context=self).get_ip_type_list(app_id, act_id, page_size, page_index, is_release, field, condition, params, order_by, is_cache=False)
        ref_params = {}
        page_info = PageInfo(page_index, page_size, total, self.business_process_executed(page_list, ref_params))
        return self.response_json_success(page_info)


class ReleaseIpTypeHandler(ClientBaseHandler):
    """
    :description: 上下架ip类型
    """
    @filter_check_params("ip_type_id")
    def get_async(self):
        """
        :description: 上下架ip类型
        :param app_id：应用标识
        :param ip_type_id: ip类型标识
        :param is_release: 是否发布 1-是 0-否
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        ip_type_id = self.get_param_int("ip_type_id", 0)
        is_release = self.get_param_int("is_release", 0)

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ip_base_model = IpBaseModel(context=self)
        invoke_result_data = ip_base_model.release_ip_type(app_id, ip_type_id, is_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()

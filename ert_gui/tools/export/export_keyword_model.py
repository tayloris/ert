#  Copyright (C) 2011  Equinor ASA, Norway.
#
#  The file 'export_keyword_model.py' is part of ERT - Ensemble based Reservoir Tool.
#
#  ERT is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
#  for more details.
from res.enkf import EnkfVarType, ErtImplType
from ert_shared import ERT


class ExportKeywordModel(object):
    def __init__(self):
        super(ExportKeywordModel, self).__init__()
        self.__gen_kw = None
        self.__field_kw = None
        self.__gen_data = None
        self.__gen_param = None

    def getKeylistFromImplType(self, ert_impl_type):
        return sorted(ERT.ert.ensembleConfig().getKeylistFromImplType(ert_impl_type))

    def isDynamicPlot(self, key):
        vtype = self.getVarType(key)
        return vtype in [EnkfVarType.DYNAMIC_STATE, EnkfVarType.DYNAMIC_RESULT]

    def isDynamicField(self, key):
        return self.getVarType(key) == EnkfVarType.DYNAMIC_STATE

    def getVarType(self, key):
        config_node = ERT.ert.ensembleConfig().getNode(key)
        variable_type = config_node.getVariableType()
        return variable_type

    def getImplementationType(self, key):
        config_node = ERT.ert.ensembleConfig().getNode(key)
        return config_node.getImplementationType()

    def getGenKwKeyWords(self):
        if self.__gen_kw is None:
            self.__gen_kw = [key for key in ERT.ert.ensembleConfig().getKeylistFromImplType(ErtImplType.GEN_KW)]

        return self.__gen_kw

    def getGenDataKeyWords(self):
        if self.__gen_data is None:
            gen_data_list = []
            gen_param_list = []
            for key in ERT.ert.ensembleConfig().getKeylistFromImplType(ErtImplType.GEN_DATA):
                if self.getVarType(key) == EnkfVarType.PARAMETER:
                    gen_param_list.append(key)
                    continue
                if ERT.ert.ensembleConfig().getNode(key).getDataModelConfig().getOutputFormat() is not None:
                    gen_data_list.append(key)
                elif ERT.ert.ensembleConfig().getNode(key).getDataModelConfig().getInputFormat() is not None:
                    gen_data_list.append(key)
            self.__gen_data = gen_data_list
            self.__gen_param = gen_param_list
        return self.__gen_data + self.__gen_param

    def getFieldKeyWords(self):
        if self.__field_kw is None:
            self.__field_kw = self.getKeylistFromImplType(ErtImplType.FIELD)

        return self.__field_kw

    def getKeyWords(self):
        return sorted(self.getFieldKeyWords() + self.getGenKwKeyWords() + self.getGenDataKeyWords())

    def hasKeywords(self):
        return len(self.getKeyWords()) > 0

    def isGenKw(self, key):
        if self.__gen_kw is None:
            self.getGenKwKeyWords()

        return key in self.__gen_kw

    def isFieldKw(self, key):
        if self.__field_kw is None:
            self.getFieldKeyWords()

        return key in self.__field_kw

    def isGenDataKw(self, key):
        if self.__gen_data is None:
            self.getGenDataKeyWords()

        return key in self.__gen_data

    def isGenParamKw(self, key):
        if self.__gen_param is None:
            self.getGenDataKeyWords()

        return key in self.__gen_param

    def getGenDataReportSteps(self, key):
        gen_data_list = []
        obs_keys = ERT.ert.ensembleConfig().getNode(key).getObservationKeys()
        for obs_key in obs_keys:
            obs_vector = ERT.ert.getObservations()[obs_key]
            for report_step in obs_vector.getStepList():
                gen_data_list.append(str(report_step))

        return gen_data_list

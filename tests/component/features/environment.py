from airflowbigdataoperators.com.kenshoo.shared_tests.component.features.environment import _before_feature, \
    _after_scenario, _before_all


def before_all(context):
    _before_all(context)


def before_feature(context, feature):
    _before_feature(context, feature)


def after_scenario(context, scenario):
    _after_scenario(context, scenario)

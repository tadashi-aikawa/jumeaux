# -*- coding:utf-8 -*-


def main(report, config):
    print("Hello!!")
    return report


def change_title(report, config):
    report.title = f"Hello!! {report.title}"\
        if config['locate_prefix'] else f"{report.title} Hello!!"
    return report

import os
import sys
import common


RACK_SDK = os.path.abspath("Rack-SDK")
STAGE_DIR = "stage"



def stage_package(plugin_dir):
	common.system(f'mkdir -p {STAGE_DIR}')
	common.system(f'mv {plugin_dir}/dist/*.zip {STAGE_DIR}/')


def delete_stage():
	common.system(f'rm -rf {STAGE_DIR}')


def build_mac(plugin_dir):
	print(f"Building {plugin_dir} for mac")
	env = f'CC=x86_64-apple-darwin17-clang CXX=x86_64-apple-darwin17-clang++-libc++ STRIP=x86_64-apple-darwin17-strip RACK_DIR={RACK_SDK}'
	make = f'{env} make -j$(nproc) -C {plugin_dir}'
	common.system(f'{make} clean')
	common.system(f'{make} cleandep')
	common.system(f'{make} dep')
	common.system(f'{make} dist')
	stage_package(plugin_dir)
	common.system(f'{make} clean')
	print(f"Built {plugin_dir} for mac")


def build_win(plugin_dir):
	print(f"Building {plugin_dir} for win")
	env = f'CC=x86_64-w64-mingw32-gcc CXX=x86_64-w64-mingw32-g++ STRIP=x86_64-w64-mingw32-strip RACK_DIR={RACK_SDK}'
	make = f'{env} make -j$(nproc) -C {plugin_dir}'
	common.system(f'{make} clean')
	common.system(f'{make} cleandep')
	common.system(f'{make} dep')
	common.system(f'{make} dist')
	stage_package(plugin_dir)
	common.system(f'{make} clean')
	print(f"Built {plugin_dir} for win")


def build_lin(plugin_dir):
	print(f"Building {plugin_dir} for lin")
	make = f'make -j$(nproc)'
	plugin_abs = os.path.abspath(plugin_dir)
	# TODO Make this Docker image publicly available
	# It's essentially just Ubuntu 16.04 with plugin build dependencies installed, the workdir, and a user account set up so it matches my own machine's UID to solve file permissions issues.
	docker = f'docker run --rm -v {RACK_SDK}:/Rack-SDK -v {plugin_abs}:/workdir -w /workdir -u vortico -e RACK_DIR=/Rack-SDK rackplugin:1'
	common.system(f'{docker} {make} clean')
	common.system(f'{docker} {make} cleandep')
	common.system(f'{docker} {make} dep')
	common.system(f'{docker} {make} dist')
	stage_package(plugin_dir)
	common.system(f'{docker} {make} clean')
	print(f"Built {plugin_dir} for lin")


def build(plugin_dir):
	build_lin(plugin_dir)
	build_mac(plugin_dir)
	build_win(plugin_dir)


if __name__ == "__main__":
	plugin_dir = sys.argv[1]
	if not plugin_dir:
		raise "No plugin_dir given"
	build(plugin_dir)


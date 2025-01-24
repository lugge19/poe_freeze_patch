import psutil
import time


def wait_in_exe(t: int = 5):
    for i in range(t, 0, -1):
        print(f"window closes in {i} seconds...")
        time.sleep(1)


def entrypoint(func):
    try:
        func()
    except Exception as e:
        print(type(e), e)
    finally:
        wait_in_exe()


def get_pid_by_name(process_name):

    pids = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                pids.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return pids


def set_cpu_affinity(pid):
    """
    Sets the CPU affinity of a process to all cores except core 0 and core 1.

    :param pid: Process ID of the target process.
    :raises: ValueError if the PID is invalid or an error occurs setting affinity.
    """
    try:
        # Get the process object
        process = psutil.Process(pid)

        # Get the total number of CPUs
        total_cpus = psutil.cpu_count()  # 16 for the ryzen 7 3700x
        if total_cpus <= 2:
            raise ValueError(
                "System does not have enough CPUs to exclude core 0 and core 1.")

        # Generate the CPU mask excluding core 0 and core 1
        cpu_mask = list(range(2, total_cpus))

        # Set the CPU affinity
        process.cpu_affinity(cpu_mask)

        print(
            f"Successfully set CPU affinity for process {pid} to cores: {cpu_mask}")
    except psutil.NoSuchProcess:
        raise ValueError(f"No process found with PID {pid}.")
    except psutil.AccessDenied:
        raise ValueError(
            f"Access denied to modify the CPU affinity of PID {pid}. Run as administrator.")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")


def main():
    process_name = "PathOfExileSteam.exe"
    pids = get_pid_by_name(process_name)

    total_cpus = psutil.cpu_count()  # 16 for the ryzen 7 3700x
    print(f"number of total cpu cores (physical + logical): {total_cpus}")

    if len(pids) == 0:
        print(f"no process for {process_name} found -> EXIT")
        return
    elif len(pids) > 1:
        print(f"found multiple processes for {process_name} -> BUG")
        return

    print(f"Process '{process_name}' found with PID(s): {pids}")  # nopep8
    pid = pids[0]
    set_cpu_affinity(pid)


if __name__ == "__main__":
    entrypoint(main)

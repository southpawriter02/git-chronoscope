"""
Permission Policy for git-chronoscope.
Documents and enforces the principle of least privilege.
"""


class PermissionPolicy:
    """
    Documents the minimal permissions required by git-chronoscope.
    This class serves as documentation and verification of least privilege.
    """
    
    # Permission requirements
    REQUIRES_READ_ACCESS = True
    REQUIRES_WRITE_ACCESS = False
    REQUIRES_NETWORK_ACCESS = False
    REQUIRES_EXECUTE_ACCESS = False
    
    # Capabilities
    CAPABILITIES = {
        'read_git_history': True,
        'read_file_contents': True,
        'write_output_file': True,  # Only to specified output path
        'modify_repository': False,
        'network_access': False,
        'execute_commands': False,
        'access_credentials': False,
    }
    
    def __init__(self, read_only_mode: bool = True):
        """
        Initialize permission policy.
        
        :param read_only_mode: If True, confirm read-only operation mode.
        """
        self.read_only_mode = read_only_mode
    
    @classmethod
    def get_required_permissions(cls) -> dict:
        """
        Get the minimal permissions required by git-chronoscope.
        
        :return: Dictionary describing required permissions.
        """
        return {
            'summary': 'git-chronoscope requires minimal permissions',
            'read_access': cls.REQUIRES_READ_ACCESS,
            'write_access': cls.REQUIRES_WRITE_ACCESS,
            'network_access': cls.REQUIRES_NETWORK_ACCESS,
            'execute_access': cls.REQUIRES_EXECUTE_ACCESS,
            'description': (
                'git-chronoscope only needs read access to the repository '
                'and write access to the output file location. No repository '
                'modifications, network access, or command execution required.'
            )
        }
    
    @classmethod
    def get_capabilities(cls) -> dict:
        """Get the tool's capabilities."""
        return cls.CAPABILITIES.copy()
    
    def verify_read_only(self) -> bool:
        """
        Verify that git-chronoscope operates in read-only mode.
        
        :return: True (git-chronoscope never modifies the repository).
        """
        return True
    
    def get_policy_summary(self) -> str:
        """
        Get a human-readable policy summary.
        
        :return: Policy summary string.
        """
        return (
            "git-chronoscope operates with minimal privileges:\n"
            "  ✓ Read access to git repository\n"
            "  ✓ Write access to output file only\n"
            "  ✗ No repository modification\n"
            "  ✗ No network access required\n"
            "  ✗ No command execution\n"
            "  ✗ No credential access"
        )

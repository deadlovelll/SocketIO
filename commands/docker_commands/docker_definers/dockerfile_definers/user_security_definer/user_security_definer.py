import textwrap

class UserSecurityDefiner:
    
    @staticmethod
    def define_user_security (
        use_nonroot_user: bool,
    ) -> str:
        
        return textwrap.dedent("""
            RUN useradd -m nonroot && chown -R nonroot:nonroot /app
            USER nonroot
""") if use_nonroot_user else ""
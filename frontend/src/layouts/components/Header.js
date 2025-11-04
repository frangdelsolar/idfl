import { AppBar, Toolbar, Typography } from '@mui/material';

function Header() {
    return (
        <AppBar position="static" elevation={2}>
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Product Certification
                </Typography>
            </Toolbar>
        </AppBar>
    );
}

export default Header;

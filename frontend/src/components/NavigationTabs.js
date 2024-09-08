import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Tabs, Tab, Button, Menu, MenuItem } from '@mui/material';

function NavigationTabs() {
  const location = useLocation(); // Hook to get the current route location
  const currentPath = location.pathname;
  const [anchorEl, setAnchorEl] = useState(null);

  // Handle dropdown menu open/close
  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <Tabs value={currentPath} textColor="inherit" indicatorColor="secondary">
      <Tab label="File Upload" value="/fileUpload" component={Link} to="/fileUpload" />
      <Tab label="Pair" value="/pair" component={Link} to="/pair" />
      <Tab label="Export Lessons" value="/export-lessons" component={Link} to="/export-lessons" />
      <Button
        aria-controls="management-menu"
        aria-haspopup="true"
        onClick={handleMenuOpen}
        style={{ textTransform: 'none', color: 'inherit' }}
      >
        Management
      </Button>
      <Menu
        id="management-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleMenuClose} component={Link} to="/instructors">Instructors</MenuItem>
        <MenuItem onClick={handleMenuClose} component={Link} to="/swimmers">Swimmers</MenuItem>
        <MenuItem onClick={handleMenuClose} component={Link} to="/lessons">Lessons</MenuItem>
      </Menu>
    </Tabs>
  );
}

export default NavigationTabs;